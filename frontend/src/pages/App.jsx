import { Backdrop, CircularProgress } from "@mui/material";
import Home from "./Home";
import { useState } from "react";
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import DocumentPreview from "./DocumentPreview";

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

const lightTheme = createTheme({
  palette: {
    mode: 'light',
  },
});

function App() {

  const [preview, setPreview] = useState(null);
  const [queryTokens, setQueryTokens] = useState([]);
  const [theme, setTheme] = useState(darkTheme);
  const [showLoader, setShowLoader] = useState(false);

  const switchTheme = () => {
    if (theme.palette.mode === 'dark') {
      setTheme(lightTheme);
    } else {
      setTheme(darkTheme);
    }
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Home setPreview={setPreview} setShowLoader={setShowLoader} setQueryTokens={setQueryTokens} theme={{theme, switchTheme}} />
      <DocumentPreview preview={preview} setPreview={setPreview} queryTokens={queryTokens} />
      <Backdrop
        sx={{ position:'absolute', color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={showLoader}
      >
        <CircularProgress color="inherit" />
      </Backdrop>
    </ThemeProvider>
  );
}

export default App;