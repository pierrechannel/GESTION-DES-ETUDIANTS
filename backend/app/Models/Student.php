<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;
class Student extends Model {
    protected $fillable = ['school_class_id', 'registration_number', 'first_name', 'last_name', 'email', 'phone', 'birth_date', 'status'];
    public function schoolClass() { return $this->belongsTo(SchoolClass::class); }
    public function grades() { return $this->hasMany(Grade::class); }
}
