import { useState } from 'react';
import Paper from '@mui/material/Paper';
import InputBase from '@mui/material/InputBase';
import IconButton from '@mui/material/IconButton';
import SearchIcon from '@mui/icons-material/Search';
import './SearchBar.css';
import { FormControl, FormControlLabel, FormLabel, Grid, Radio, RadioGroup, Typography } from '@mui/material';

function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('');
  const [searchModel, setSearchModel] = useState('bm25');

  const handleSearch = (event) => {
    event.preventDefault();
    onSearch({ query, searchModel });
  };

  return (
        <Paper
          sx={{ p: '2px 4px', display: 'flex', alignItems: 'center' }}
        >
          <InputBase
            sx={{ flex: 1, ml: 1, minWidth: '40vw'}}
            placeholder="Enter text to search..."
            inputProps={{ 'aria-label': 'search' }}
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === 'Enter') {
                handleSearch(event);
              }
            }}
          />
          <IconButton type="button" sx={{ p: '10px' }} aria-label="search" onClick={handleSearch}>
            <SearchIcon />
          </IconButton>
        </Paper>
  );
}

export default SearchBar;