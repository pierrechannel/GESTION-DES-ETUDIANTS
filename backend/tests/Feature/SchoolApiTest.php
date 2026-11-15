<?php
namespace Tests\Feature;
use App\Models\{User, Program, SchoolClass, Subject, Student, Grade};
use Illuminate\Foundation\Testing\RefreshDatabase;
use Laravel\Sanctum\Sanctum;
use Tests\TestCase;
class SchoolApiTest extends TestCase {
    use RefreshDatabase;
    private function school(): array {
        $p = Program::create(['name' => 'Software', 'code' => 'GL']);
        $c = SchoolClass::create(['name' => 'L1', 'program_id' => $p->id, 'academic_year' => '2026-2027']);
        $s = Student::create(['first_name' => 'Aline', 'last_name' => 'Ndayi', 'registration_number' => 'ETU-1', 'school_class_id' => $c->id, 'status' => 'active']);
        $m = Subject::create(['name' => 'Algorithms', 'code' => 'ALG', 'school_class_id' => $c->id, 'coefficient' => 3]);
        return [$p, $c, $s, $m];
    }
    private function admin(): void { Sanctum::actingAs(User::factory()->create(['role' => 'admin'])); }
    public function test_guests_cannot_access_school_records(): void {
        $this->getJson('/api/v1/students')->assertUnauthorized();
    }
    public function test_registration_does_not_allow_admin_role_and_logout_revokes_token(): void {
        $response = $this->postJson('/api/v1/register', ['name' => 'Reader', 'email' => 'reader@example.test', 'password' => 'TestPass123!', 'password_confirmation' => 'TestPass123!', 'role' => 'admin'])->assertCreated()->assertJsonPath('user.role', 'user');
        $token = $response->json('token');
        $this->withToken($token)->getJson('/api/v1/me')->assertOk();
        $this->withToken($token)->postJson('/api/v1/logout')->assertNoContent();
        $this->assertDatabaseCount('personal_access_tokens', 0);
    }
    public function test_login_checks_password_and_hashes_storage(): void {
        $user = User::factory()->create(['password' => 'TestPass123!']);
        $this->assertNotEquals('TestPass123!', $user->password);
        $this->postJson('/api/v1/login', ['email' => $user->email, 'password' => 'wrong'])->assertUnprocessable();
        $this->postJson('/api/v1/login', ['email' => $user->email, 'password' => 'TestPass123!'])->assertOk()->assertJsonStructure(['token', 'user']);
    }
    public function test_readers_can_read_but_cannot_modify(): void {
        [$p, $c, $s] = $this->school();
        Sanctum::actingAs(User::factory()->create(['role' => 'user']));
        $this->getJson('/api/v1/students')->assertOk()->assertJsonPath('total', 1);
        $this->postJson('/api/v1/programs', ['name' => 'Other', 'code' => 'X'])->assertForbidden();
        $this->putJson('/api/v1/students/'.$s->id, $s->toArray())->assertForbidden();
        $this->deleteJson('/api/v1/students/'.$s->id)->assertForbidden();
    }
    public function test_student_crud_unique_number_and_detail(): void {
        [$p, $c] = $this->school(); $this->admin();
        $data = ['first_name' => 'David', 'last_name' => 'Niyo', 'registration_number' => 'ETU-2', 'school_class_id' => $c->id, 'status' => 'active'];
        $id = $this->postJson('/api/v1/students', $data)->assertCreated()->json('id');
        $this->postJson('/api/v1/students', $data)->assertUnprocessable()->assertJsonValidationErrors('registration_number');
        $this->getJson('/api/v1/students/'.$id)->assertOk()->assertJsonPath('first_name', 'David');
        $this->putJson('/api/v1/students/'.$id, [...$data, 'first_name' => 'Eric'])->assertOk()->assertJsonPath('first_name', 'Eric');
        $this->deleteJson('/api/v1/students/'.$id)->assertNoContent();
        $this->getJson('/api/v1/students/'.$id)->assertNotFound();
    }
    public function test_search_filter_and_pagination_on_two_lists(): void {
        [$p, $c, $s, $m] = $this->school(); $this->admin();
        Grade::create(['student_id' => $s->id, 'subject_id' => $m->id, 'assessment' => 'Exam', 'score' => 15, 'weight' => 1]);
        $this->getJson('/api/v1/students?search=Ndayi&program_id='.$p->id.'&per_page=1')->assertOk()->assertJsonPath('total', 1)->assertJsonCount(1, 'data');
        $this->getJson('/api/v1/students?program_id=9999')->assertJsonPath('total', 0);
        $this->getJson('/api/v1/grades?search=Exam&subject_id='.$m->id.'&per_page=1')->assertOk()->assertJsonPath('total', 1);
        $this->getJson('/api/v1/grades?search=Unknown')->assertJsonPath('total', 0);
    }
    public function test_weighted_averages_and_missing_grades(): void {
        [$p, $c, $s, $m] = $this->school(); $this->admin();
        Grade::create(['student_id' => $s->id, 'subject_id' => $m->id, 'assessment' => 'Test', 'score' => 10, 'weight' => 1]);
        Grade::create(['student_id' => $s->id, 'subject_id' => $m->id, 'assessment' => 'Exam', 'score' => 18, 'weight' => 3]);
        $m2 = Subject::create(['name' => 'English', 'code' => 'ENG', 'school_class_id' => $c->id, 'coefficient' => 1]);
        $this->getJson('/api/v1/students/'.$s->id.'/transcript')->assertOk()->assertJsonPath('general_average', 16)->assertJsonPath('complete', false);
        Grade::create(['student_id' => $s->id, 'subject_id' => $m2->id, 'assessment' => 'Exam', 'score' => 12, 'weight' => 1]);
        $this->getJson('/api/v1/students/'.$s->id.'/transcript')->assertJsonPath('general_average', 15)->assertJsonPath('complete', true);
    }
    public function test_invalid_grade_and_foreign_class_are_rejected(): void {
        [$p, $c, $s, $m] = $this->school(); $this->admin();
        $data = ['student_id' => $s->id, 'subject_id' => $m->id, 'assessment' => 'Exam', 'score' => 21, 'weight' => 1];
        $this->postJson('/api/v1/grades', $data)->assertUnprocessable()->assertJsonValidationErrors('score');
        $other = SchoolClass::create(['name' => 'L2', 'program_id' => $p->id, 'academic_year' => '2026-2027']);
        $m->update(['school_class_id' => $other->id]);
        $this->postJson('/api/v1/grades', [...$data, 'score' => 15])->assertUnprocessable()->assertJsonValidationErrors('subject_id');
    }
    public function test_dependencies_and_class_changes_are_protected(): void {
        [$p, $c, $s, $m] = $this->school(); $this->admin();
        Grade::create(['student_id' => $s->id, 'subject_id' => $m->id, 'assessment' => 'Exam', 'score' => 15, 'weight' => 1]);
        $other = SchoolClass::create(['name' => 'L2', 'program_id' => $p->id, 'academic_year' => '2026-2027']);
        $this->putJson('/api/v1/students/'.$s->id, [...$s->toArray(), 'school_class_id' => $other->id])->assertUnprocessable();
        $this->putJson('/api/v1/subjects/'.$m->id, [...$m->toArray(), 'school_class_id' => $other->id])->assertUnprocessable();
        $this->deleteJson('/api/v1/classes/'.$c->id)->assertConflict();
        $this->deleteJson('/api/v1/students/'.$s->id)->assertNoContent();
        $this->assertDatabaseCount('grades', 0);
    }
    public function test_program_class_subject_and_grade_crud(): void {
        $this->admin();
        $p = $this->postJson('/api/v1/programs', ['name' => 'Finance', 'code' => 'FIN'])->assertCreated()->json();
        $this->putJson('/api/v1/programs/'.$p['id'], [...$p, 'name' => 'Business'])->assertOk();
        $c = $this->postJson('/api/v1/classes', ['name' => 'L1', 'program_id' => $p['id'], 'academic_year' => '2026-2027'])->assertCreated()->json();
        $this->putJson('/api/v1/classes/'.$c['id'], [...$c, 'name' => 'L2'])->assertOk();
        $m = $this->postJson('/api/v1/subjects', ['name' => 'Math', 'code' => 'MATH', 'school_class_id' => $c['id'], 'coefficient' => 2])->assertCreated()->json();
        $this->putJson('/api/v1/subjects/'.$m['id'], [...$m, 'coefficient' => 3])->assertOk();
        $s = Student::create(['first_name' => 'Test', 'last_name' => 'Person', 'registration_number' => 'NEW', 'school_class_id' => $c['id'], 'status' => 'active']);
        $g = $this->postJson('/api/v1/grades', ['student_id' => $s->id, 'subject_id' => $m['id'], 'assessment' => 'Exam', 'score' => 13, 'weight' => 1])->assertCreated()->json();
        $this->putJson('/api/v1/grades/'.$g['id'], [...$g, 'score' => 17])->assertOk();
        $this->deleteJson('/api/v1/grades/'.$g['id'])->assertNoContent();
        $this->deleteJson('/api/v1/subjects/'.$m['id'])->assertNoContent();
        $this->deleteJson('/api/v1/students/'.$s->id)->assertNoContent();
        $this->deleteJson('/api/v1/classes/'.$c['id'])->assertNoContent();
        $this->deleteJson('/api/v1/programs/'.$p['id'])->assertNoContent();
    }
}
