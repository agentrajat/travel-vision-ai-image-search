import * as React from 'react';
import { styled } from '@mui/material/styles';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import Typography from '@mui/material/Typography';
import { Box, Grid, LinearProgress, linearProgressClasses } from '@mui/material';
import AI_ICON from '../assets/images/ai_image.svg';

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
  '& .MuiDialogContent-root': {
    padding: theme.spacing(2),
  },
  '& .MuiDialogActions-root': {
    padding: theme.spacing(1),
  },
}));

const BorderLinearProgress = styled(LinearProgress)(({ theme }) => ({
  height: 10,
  borderRadius: 5,
  [`& .${linearProgressClasses.bar}`]: {
    borderRadius: 5
  }
}));

// const viewDate = (timestamp) => {
//   const date = new Date(timestamp);
//   // Format the date to be displayed in the format "dd/mm/yyyy hh:mm:ss AM/PM"
//   return date.toLocaleString('en-US');
// }

export default function DocumentPreview({preview, setPreview, queryTokens}) {
  const open = (preview !== null);

  const handleClose = () => {
    setPreview(null);
  };

  const getCV = () => {
    if (preview === null || preview.cv === null || preview.cv.length === 0) {
      return [];
    }
    return preview.cv;
  }

  return (
      <BootstrapDialog
        onClose={handleClose}
        aria-labelledby="customized-dialog-title"
        open={open}
        maxWidth='lg'
      >
        {preview ? (<>
        <DialogTitle sx={{ m: 0, p: 2 }} id="customized-dialog-title">
          @{preview.group}
        </DialogTitle>
        <IconButton
          aria-label="close"
          onClick={handleClose}
          sx={{
            position: 'absolute',
            right: 8,
            top: 8,
            color: (theme) => theme.palette.grey[500],
          }}
        >
          <CloseIcon />
        </IconButton>
        <DialogContent dividers>
          <Grid container>
            <Grid item xs>
              <img
                src={preview.static_link}
                alt={preview.label}
                style={{width: '100%', borderRadius: 5}}
              />
            </Grid>
            <Grid item xs sx={{pl: 3, pr: 3}}>
              {/* <Chip label={"Scrapped On: " + viewDate(preview.scrap_time * 1000)} sx={{mb: 1}} /> */}
              <Typography variant='h6' gutterBottom>
                {preview.label}
              </Typography>
              <img src={AI_ICON} alt="AI" style={{width: 16, height: 16}} />
              <Typography variant='subtitle1' sx={{display: 'inline', ml: 1}}>
                Generated Caption:
              </Typography>
              <Typography variant='subtitle1' gutterBottom color="orange" sx={{ml: 3}}>
                {preview.caption}
              </Typography>
              <img src={AI_ICON} alt="AI" style={{width: 16, height: 16}} />
              <Typography variant='subtitle1' gutterBottom sx={{display: 'inline', ml: 1}}>
                Image Classification Score:
              </Typography>
              <Box sx={{ml: 3, mb: 1}}>
                {getCV().map((cv, index) => (
                    <Box key={index} sx={{mt: 1}}>
                      <Typography variant="body2" color="text.secondary" sx={{flex: 1}} gutterBottom>
                        ({cv.score.toFixed(8)}) - {cv.label}
                      </Typography>
                      <Box sx={{ width: '100%', mr: 1 }}>
                        <BorderLinearProgress color='secondary' variant="determinate" value={cv.score * 100} />
                      </Box>
                    </Box>
                ))}
              </Box>
            </Grid>
          </Grid>
        </DialogContent></>) : <></>}
      </BootstrapDialog>
  );
}
