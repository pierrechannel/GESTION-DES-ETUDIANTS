<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;
class Subject extends Model {
    protected $fillable = ['name', 'code', 'school_class_id', 'coefficient'];
    public function schoolClass() { return $this->belongsTo(SchoolClass::class); }
    public function grades() { return $this->hasMany(Grade::class); }
}
