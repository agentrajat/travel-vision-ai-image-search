import { Box, Chip, Grid, IconButton, ImageList, ImageListItem, ImageListItemBar, Link, Paper, Typography } from "@mui/material";
import InfoIcon from '@mui/icons-material/Info';

const LABEL_LENGTH = 30;

function truncateLabel(label) {
  if (label.length > LABEL_LENGTH) {
    return label.substring(0, LABEL_LENGTH) + '...';
  }
  return label;
}

const openInNewTab = (url) => {
  const newWindow = window.open(url, '_blank', 'noopener,noreferrer')
  if (newWindow) newWindow.opener = null
}

function Result({ result, setPreview }) {
  return (
    <Grid container alignItems="baseline" justifyContent="center">
    {result.map((elem, index) => (
      elem.document ? (
        <Grid item key={index} sx={{m:2, position:'relative', lineHeight: 0}}>
          <img
            src={elem.document.static_link}
            alt={elem.document.label}
            style={{maxHeight: 240, cursor: 'pointer', lineHeight: 0, minWidth: 240, minHeight: 240}}
            onClick={() => openInNewTab(elem.document.link)}
            loading="lazy"  
          />
          <Paper sx={{lineHeight: 1.5, position: 'absolute', bottom: 0, display: 'flex', alignItems: 'center', width: '100%', borderRadius: 0, opacity: 0.9}}>
            <Box sx={{display: 'flex', flex: 1, flexDirection: 'column', pl: 1, pt: 1, pb: 1}}>
              <Typography variant="body2" sx={{fontSize: 10, flex: 1}}>{<span>@{elem.document.group}</span>}</Typography>
              <Link underline="hover" onClick={() => openInNewTab(elem.document.link)} sx={{cursor: 'pointer'}}>
                {truncateLabel(elem.document.label)}
              </Link>
            </Box>
            <IconButton onClick={() => setPreview(elem.document)}>
              <InfoIcon/>
            </IconButton>
          </Paper>
        </Grid>
      ) : <></>
    ))}
    </Grid>
  );
}

export default Result;