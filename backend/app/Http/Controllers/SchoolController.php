<?php
namespace App\Http\Controllers;
use App\Models\{Program, SchoolClass, Subject, Student, Grade};
use App\Services\TranscriptService;
use Illuminate\Http\Request;
use Illuminate\Validation\Rule;
use Illuminate\Validation\ValidationException;
use Illuminate\Database\QueryException;
class SchoolController extends Controller {
    private const MODELS = ['programs' => Program::class, 'classes' => SchoolClass::class, 'subjects' => Subject::class, 'students' => Student::class, 'grades' => Grade::class];
    private function model(string $entity): string { abort_unless(isset(self::MODELS[$entity]), 404); return self::MODELS[$entity]; }
    private function query(string $entity) {
        return match ($entity) {
            'students' => Student::with('schoolClass.program'), 'classes' => SchoolClass::with('program')->withCount('students'),
            'subjects' => Subject::with('schoolClass.program'), 'grades' => Grade::with(['student', 'subject']), default => Program::withCount('classes'),
        };
    }
    public function index(Request $request, string $entity) {
        $this->model($entity); $query = $this->query($entity);
        if ($search = $request->query('search')) $query->where(function ($q) use ($entity, $search) {
            $fields = match ($entity) { 'students' => ['first_name', 'last_name', 'registration_number'], 'grades' => ['assessment'], 'classes' => ['name', 'academic_year'], default => ['name', 'code'] };
            foreach ($fields as $field) $q->orWhere($field, 'like', '%'.$search.'%');
            if ($entity === 'grades') $q->orWhereHas('student', fn ($s) => $s->where('last_name', 'like', '%'.$search.'%')->orWhere('registration_number', 'like', '%'.$search.'%'));
        });
        if ($entity === 'students') {
            if ($request->filled('program_id')) $query->whereHas('schoolClass', fn ($q) => $q->where('program_id', $request->program_id));
            if ($request->filled('class_id')) $query->where('school_class_id', $request->class_id);
            if ($request->filled('status')) $query->where('status', $request->status);
        }
        if ($entity === 'classes' && $request->filled('program_id')) $query->where('program_id', $request->program_id);
        if ($entity === 'subjects' && $request->filled('class_id')) $query->where('school_class_id', $request->class_id);
        if ($entity === 'grades') {
            if ($request->filled('student_id')) $query->where('student_id', $request->student_id);
            if ($request->filled('subject_id')) $query->where('subject_id', $request->subject_id);
        }
        return $query->orderByDesc('id')->paginate(min(100, max(1, (int) $request->query('per_page', 10))));
    }
    public function show(string $entity, int $id) { $this->model($entity); return $this->query($entity)->findOrFail($id); }
    private function validated(Request $request, string $entity, $record = null): array {
        $unique = fn ($table, $column) => Rule::unique($table, $column)->ignore($record?->id);
        $rules = match ($entity) {
            'programs' => ['name' => 'required|string|max:150', 'code' => ['required', 'string', 'max:30', $unique('programs', 'code')], 'description' => 'nullable|string|max:2000'],
            'classes' => ['name' => ['required', 'string', 'max:150', Rule::unique('school_classes')->where(fn ($q) => $q->where('program_id', $request->program_id)->where('academic_year', $request->academic_year))->ignore($record?->id)], 'program_id' => 'required|exists:programs,id', 'academic_year' => ['required', 'regex:/^\d{4}-\d{4}$/']],
            'subjects' => ['name' => 'required|string|max:150', 'code' => ['required', 'string', 'max:30', $unique('subjects', 'code')], 'school_class_id' => 'required|exists:school_classes,id', 'coefficient' => 'required|numeric|min:0.01|max:100'],
            'students' => ['registration_number' => ['required', 'string', 'max:40', $unique('students', 'registration_number')], 'first_name' => 'required|string|max:100', 'last_name' => 'required|string|max:100', 'email' => ['nullable', 'email', 'max:255', $unique('students', 'email')], 'phone' => 'nullable|string|max:30', 'birth_date' => 'nullable|date|before_or_equal:today', 'school_class_id' => 'required|exists:school_classes,id', 'status' => 'required|in:active,inactive'],
            'grades' => ['student_id' => 'required|exists:students,id', 'subject_id' => 'required|exists:subjects,id', 'assessment' => ['required', 'string', 'max:100', Rule::unique('grades')->where(fn ($q) => $q->where('student_id', $request->student_id)->where('subject_id', $request->subject_id))->ignore($record?->id)], 'score' => 'required|numeric|min:0|max:20', 'weight' => 'required|numeric|min:0.01|max:100'],
        };
        $data = $request->validate($rules);
        if ($entity === 'grades' && Student::findOrFail($data['student_id'])->school_class_id !== Subject::findOrFail($data['subject_id'])->school_class_id) throw ValidationException::withMessages(['subject_id' => ['La matière doit appartenir à la classe de cet étudiant.']]);
        if ($entity === 'students' && $record && $record->school_class_id != $data['school_class_id'] && $record->grades()->exists()) throw ValidationException::withMessages(['school_class_id' => ['Retirez les notes avant de changer la classe.']]);
        if ($entity === 'subjects' && $record && $record->school_class_id != $data['school_class_id'] && $record->grades()->exists()) throw ValidationException::withMessages(['school_class_id' => ['Une matière notée ne peut pas changer de classe.']]);
        return $data;
    }
    public function store(Request $request, string $entity) {
        $model = $this->model($entity); $record = $model::create($this->validated($request, $entity));
        return response()->json($this->query($entity)->find($record->id), 201);
    }
    public function update(Request $request, string $entity, int $id) {
        $model = $this->model($entity); $record = $model::findOrFail($id); $record->update($this->validated($request, $entity, $record)); return $this->query($entity)->find($id);
    }
    public function destroy(string $entity, int $id) {
        $model = $this->model($entity);
        try { $model::findOrFail($id)->delete(); } catch (QueryException $e) {
            if (in_array($e->getCode(), ['23000', '23503'])) return response()->json(['message' => 'Suppression impossible : des données dépendent de cet élément.'], 409);
            throw $e;
        }
        return response()->noContent();
    }
    public function transcript(Student $student, TranscriptService $service) { return $service->forStudent($student); }
    public function dashboard() {
        // Six calendar months, including months without registrations, in local campus time.
        $now = \Carbon\CarbonImmutable::now('Africa/Bujumbura');
        $start = $now->startOfMonth()->subMonths(5);
        $registrations = Student::whereBetween('created_at', [$start->utc(), $now->utc()])
            ->get(['created_at'])
            ->groupBy(fn ($student) => $student->created_at->timezone('Africa/Bujumbura')->format('Y-m'));
        $months = collect(range(0, 5))->map(function ($offset) use ($start, $registrations) {
            $month = $start->addMonths($offset)->format('Y-m');
            return ['month' => $month, 'count' => $registrations->get($month, collect())->count()];
        });
        return ['students' => Student::count(), 'active_students' => Student::where('status', 'active')->count(), 'programs' => Program::count(), 'classes' => SchoolClass::count(), 'subjects' => Subject::count(),
            'registrations_by_month' => $months,
            'by_class' => SchoolClass::with('program')->withCount('students')->get(), 'recent_students' => Student::with('schoolClass.program')->latest()->take(5)->get()];
    }
    public function options() {
        return ['programs' => Program::orderBy('name')->get(), 'classes' => SchoolClass::with('program')->orderBy('name')->get(), 'subjects' => Subject::with('schoolClass')->orderBy('name')->get(),
            'students' => Student::select('id', 'first_name', 'last_name', 'registration_number', 'school_class_id')->orderBy('last_name')->get()];
    }
}
