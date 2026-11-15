<?php
namespace Database\Seeders;
use App\Models\{User, Program, SchoolClass, Subject, Student, Grade};
use Illuminate\Database\Seeder;
class DatabaseSeeder extends Seeder {
    public function run(): void {
        User::firstOrCreate(['email' => 'admin@campus.test'], ['name' => 'Administration', 'password' => 'Campus2026!', 'role' => 'admin']);
        User::firstOrCreate(['email' => 'lecteur@campus.test'], ['name' => 'Utilisateur', 'password' => 'Campus2026!', 'role' => 'user']);
        foreach ([['Génie logiciel', 'GL'], ['Réseaux et télécommunications', 'RT'], ['Gestion et finance', 'GF']] as [$name, $code]) {
            $program = Program::updateOrCreate(['code' => $code], ['name' => $name, 'description' => 'Formation en '.$name]);
            foreach (['Licence 1', 'Licence 2'] as $i => $level) {
                $class = SchoolClass::firstOrCreate(['program_id' => $program->id, 'name' => $level, 'academic_year' => '2026-2027']);
                foreach (['Programmation', 'Mathématiques', 'Anglais'] as $j => $subject) Subject::updateOrCreate(['code' => $code.($i + 1).'-'.($j + 1)], ['name' => $subject, 'school_class_id' => $class->id, 'coefficient' => $j === 0 ? 3 : 2]);
            }
        }
        $people = [['Aline', 'Ndayishimiye'], ['Jean', 'Nkurunziza'], ['Grâce', 'Iradukunda'], ['David', 'Niyonzima'], ['Sarah', 'Uwimana'], ['Eric', 'Hakizimana'], ['Diane', 'Nshimirimana'], ['Patrick', 'Bizimana'], ['Esther', 'Niyomwungere'], ['Kevin', 'Nsabimana'], ['Alice', 'Mugisha'], ['Emmanuel', 'Ntahomvukiye']];
        $classes = SchoolClass::with('subjects')->get();
        foreach ($people as $i => [$first, $last]) {
            $class = $classes[$i % $classes->count()];
            $student = Student::updateOrCreate(['registration_number' => 'ETU-2026-'.str_pad($i + 1, 4, '0', STR_PAD_LEFT)], ['first_name' => $first, 'last_name' => $last, 'email' => 'etudiant'.($i + 1).'@example.test', 'school_class_id' => $class->id, 'status' => 'active', 'birth_date' => '2003-05-12']);
            foreach ($class->subjects as $j => $subject) Grade::updateOrCreate(['student_id' => $student->id, 'subject_id' => $subject->id, 'assessment' => 'Contrôle continu'], ['score' => 8 + (($i + $j * 3) % 12), 'weight' => 1]);
        }
    }
}
