<?php
namespace App\Services;
use App\Models\Student;
class TranscriptService {
    public function forStudent(Student $student): array {
        $student->load(['schoolClass.program', 'schoolClass.subjects', 'grades']);
        $rows = $student->schoolClass->subjects->map(function ($subject) use ($student) {
            $grades = $student->grades->where('subject_id', $subject->id);
            $weight = $grades->sum('weight');
            return ['subject' => $subject, 'grades' => $grades->values(), 'average' => $weight ? $grades->sum(fn ($g) => $g->score * $g->weight) / $weight : null];
        });
        $graded = $rows->whereNotNull('average');
        $coefficient = $graded->sum(fn ($row) => (float) $row['subject']->coefficient);
        $average = $coefficient ? $graded->sum(fn ($row) => $row['average'] * $row['subject']->coefficient) / $coefficient : null;
        return ['student' => $student, 'subjects' => $rows, 'general_average' => $average === null ? null : round($average, 2), 'complete' => $rows->isNotEmpty() && $rows->every(fn ($row) => $row['average'] !== null)];
    }
}
