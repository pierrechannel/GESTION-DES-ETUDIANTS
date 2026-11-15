import DashboardOutlined from '@mui/icons-material/DashboardOutlined';
import PeopleOutline from '@mui/icons-material/PeopleOutline';
import AccountTreeOutlined from '@mui/icons-material/AccountTreeOutlined';
import ClassOutlined from '@mui/icons-material/ClassOutlined';
import MenuBookOutlined from '@mui/icons-material/MenuBookOutlined';
import GradingOutlined from '@mui/icons-material/GradingOutlined';

export const sections = {
  dashboard: { label: 'Vue d’ensemble', icon: DashboardOutlined },
  students: { label: 'Étudiants', singular: 'un étudiant', icon: PeopleOutline, description: 'Tous les parcours commencent par un étudiant.' },
  programs: { label: 'Filières', singular: 'une filière', icon: AccountTreeOutlined, description: 'Organisez les parcours de formation de votre établissement.' },
  classes: { label: 'Classes', singular: 'une classe', icon: ClassOutlined, description: 'Retrouvez vos classes et leurs effectifs.' },
  subjects: { label: 'Matières', singular: 'une matière', icon: MenuBookOutlined, description: 'Structurez les enseignements et leurs coefficients.' },
  grades: { label: 'Notes', singular: 'une note', icon: GradingOutlined, description: 'Suivez les résultats et la progression des étudiants.' },
};
