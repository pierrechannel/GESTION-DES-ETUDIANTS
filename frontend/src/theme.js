import { createTheme } from '@mui/material/styles';

const theme = createTheme({ palette: { primary: { main: '#215749' }, background: { default: '#f6f7f9' } }, typography: { fontFamily: 'Inter, Segoe UI, sans-serif', button: { textTransform: 'none', fontWeight: 600 } }, shape: { borderRadius: 10 }, components: { MuiButton: { defaultProps: { disableElevation: true } }, MuiTableCell: { styleOverrides: { head: { background: '#f8faf9', color: '#6b7780', fontWeight: 600 }, root: { borderColor: '#edf0f2', padding: '16px' } } } } });

export default theme;
