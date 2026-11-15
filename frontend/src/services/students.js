import api from './api';

export async function getStudentsForExport({ search = '', programId = '' } = {}) {
  const students = [];
  let page = 1;
  let result;
  do {
    const params = new URLSearchParams({
      search,
      per_page: 100,
      page,
      ...(programId ? { program_id: programId } : {}),
    });
    result = await api(`students?${params}`);
    students.push(...result.data);
    page++;
  } while (page <= result.last_page);
  return students;
}
