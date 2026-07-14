import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#3454D1",
      light: "#6C8CFF",
      dark: "#20358F",
      contrastText: "#fff",
    },
    secondary: {
      main: "#17B890",
    },
    background: {
      default: "#F4F6FB",
      paper: "#FFFFFF",
    },
    text: {
      primary: "#1A2138",
      secondary: "#5B6478",
    },
  },
  shape: {
    borderRadius: 14,
  },
  typography: {
    fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    h4: { fontWeight: 700 },
    h5: { fontWeight: 700 },
    h6: { fontWeight: 600 },
    button: { fontWeight: 600, textTransform: "none" },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          boxShadow: "0 4px 24px rgba(20, 30, 60, 0.06)",
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 10,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          border: "1px solid #EBEEF5",
        },
      },
    },
  },
});

export default theme;
