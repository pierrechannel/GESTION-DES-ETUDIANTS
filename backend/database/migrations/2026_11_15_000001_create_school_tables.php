<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
return new class extends Migration {
    public function up(): void {
        Schema::table('users', fn (Blueprint $t) => $t->string('role')->default('user'));
        Schema::create('programs', function (Blueprint $t) {
            $t->id(); $t->string('name'); $t->string('code')->unique(); $t->text('description')->nullable(); $t->timestamps();
        });
        Schema::create('school_classes', function (Blueprint $t) {
            $t->id(); $t->foreignId('program_id')->constrained()->restrictOnDelete();
            $t->string('name'); $t->string('academic_year'); $t->timestamps(); $t->unique(['program_id', 'name', 'academic_year']);
        });
        Schema::create('subjects', function (Blueprint $t) {
            $t->id(); $t->foreignId('school_class_id')->constrained()->restrictOnDelete();
            $t->string('name'); $t->string('code')->unique(); $t->decimal('coefficient', 6, 2)->default(1); $t->timestamps();
        });
        Schema::create('students', function (Blueprint $t) {
            $t->id(); $t->foreignId('school_class_id')->constrained()->restrictOnDelete();
            $t->string('registration_number')->unique(); $t->string('first_name'); $t->string('last_name');
            $t->string('email')->nullable()->unique(); $t->string('phone')->nullable(); $t->date('birth_date')->nullable();
            $t->string('status')->default('active'); $t->timestamps();
        });
        Schema::create('grades', function (Blueprint $t) {
            $t->id(); $t->foreignId('student_id')->constrained()->cascadeOnDelete();
            $t->foreignId('subject_id')->constrained()->restrictOnDelete(); $t->string('assessment');
            $t->decimal('score', 5, 2); $t->decimal('weight', 6, 2)->default(1); $t->timestamps();
            $t->unique(['student_id', 'subject_id', 'assessment']);
        });
    }
    public function down(): void {
        foreach (['grades', 'students', 'subjects', 'school_classes', 'programs'] as $table) Schema::dropIfExists($table);
        Schema::table('users', fn (Blueprint $t) => $t->dropColumn('role'));
    }
};
