<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;
class SchoolClass extends Model {
    protected $fillable = ['name', 'program_id', 'academic_year'];
    public function program() { return $this->belongsTo(Program::class); }
    public function students() { return $this->hasMany(Student::class); }
    public function subjects() { return $this->hasMany(Subject::class); }
}
