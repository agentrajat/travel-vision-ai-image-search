import { Box, Grid, Pagination, Typography } from '@mui/material';
import SearchBar from '../components/SearchBar/SearchBar';
import Result from '../components/Result/Result';
import LightMode from '@mui/icons-material/LightMode';
import DarkMode from '@mui/icons-material/DarkMode';
import IconButton from '@mui/material/IconButton';
import { fetchDocumentsAPI, initializeAPI, invokeSearchAPI } from '../services/APIService';
import { useState, useEffect } from 'react';

const PAGE_SIZE = 10;
const DEFAULT_PAGE = 1;

function Home({ setPreview, setShowLoader, setQueryTokens, theme }) {

  const [searchResults, setSearchResults] = useState([]);
  const [page, setPage] = useState(DEFAULT_PAGE);
  const [noResults, setNoResults] = useState(false);

  useEffect(() => {
    initializeAPI();
    return () => { };
  }, []);

  const invokeSearch = ({ query, searchModel }) => {
    if (query && query.length > 0) {
      setShowLoader(true);
      invokeSearchAPI({ query, searchModel }).then((data) => {
        setShowLoader(false);
        setPreview(null);
        if (data === undefined || data?.results?.length === 0) {
          setNoResults(true);
          setSearchResults([]);
          setQueryTokens([])
          return;
        } else {
          setNoResults(false);
          // const searchData = data?.results?.map((elem, index) => {
          //   return { ...elem, rank: index + 1 };
          // });
          setQueryTokens(data?.tokens);
          loadPage(DEFAULT_PAGE, data.results);
        }
      })
      .catch((error) => {
        console.error('Error while searching', error);
        setShowLoader(false);
      });
    }
  };

  const loadPage = (newPage, searchData) => {
    setPage(newPage);
    const pageStart = (newPage - 1) * PAGE_SIZE;
    const pageEnd = pageStart + PAGE_SIZE;

    let fetchingList = [];
    for (let i = pageStart; i < pageEnd; i++) {
      if (i < searchData.length && !searchData[i].document) {
        fetchingList.push(searchData[i].docno);
      }
    }

    if (fetchingList.length > 0) {
      setShowLoader(true);
      fetchDocumentsAPI(fetchingList).then((data) => {
        setShowLoader(false);
        if (data && data.length > 0) {
          const updatedResults = [...searchData];
          for (let i = 0; i < data.length; i++) {
            const docno = data[i].docno;
            const index = fetchingList.indexOf(docno);
            if (index > -1) {
              updatedResults[pageStart + index].document = data[i];
            }
          }
          setSearchResults(updatedResults);
        }
      }).catch((error) => {
        setShowLoader(false);
        console.error('Error while fetching documents', error);
      });
    }
  }

  const getPageSize = () => {
    return Math.ceil(searchResults.length / PAGE_SIZE);
  }

  const handlePageChange = (event, value) => {
    loadPage(value, searchResults);
  }

  const getCurrentPage = () => {
    const pageStart = (page - 1) * PAGE_SIZE;
    const pageEnd = pageStart + PAGE_SIZE;
    return searchResults.slice(pageStart, pageEnd);
  }

  return (
    <Box sx={{ pt: 3, pr: 3, pl: 3, height: '100vh', display: 'flex', flexDirection:'column', justifyContent: 'space-between' }}>
      <Box component="header">
        <Grid container spacing={2} alignItems="center" justifyContent="center">
          <Grid item>
            <Typography className="title-style" variant="h3">Travel Vision</Typography>
          </Grid>
          <Grid item>
            <SearchBar onSearch={invokeSearch} theme={theme} />
          </Grid>
          <Grid item>
            <IconButton type="button" sx={{ p: '10px' }} aria-label="search" onClick={theme.switchTheme}>
              {theme?.theme?.palette.mode === 'dark' ? <LightMode /> : <DarkMode />}
            </IconButton>
          </Grid>
        </Grid>
      </Box>
      <Box component="section" sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        {searchResults?.length > 0 && (<>
          <Typography sx={{ mb: 2, mt: 3 }}>Search Results (About {searchResults.length} images found)</Typography>
          <Result result={getCurrentPage()} setPreview={setPreview} />
          <Pagination sx={{ mt: 3 }} count={getPageSize()} defaultPage={1} page={page} onChange={handlePageChange} />
        </>)}
        {noResults && (
          <Typography variant="h6" sx={{ mt: 3 }}>No results found</Typography>
        )}
      </Box>
      <Box component="footer">
        <Typography variant="body2" align="center" sx={{mt: 3, mb: 2}}>CA6005 Assignment 2 | Rajat Lashkare | © 2024 Travel Vision | All images are taken form <a href='<<website_url>>'>Website Name Here...</a></Typography>
      </Box>  
    </Box>
  );
}

export default Home;
