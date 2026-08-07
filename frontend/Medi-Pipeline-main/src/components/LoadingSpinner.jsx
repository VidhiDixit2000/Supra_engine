import { Box, CircularProgress, Typography } from '@mui/material';

const LoadingSpinner = ({ message = 'Loading...' }) => (
  <Box alignItems="center" display="flex" flexDirection="column" gap={2} justifyContent="center" py={6}>
    <CircularProgress />
    <Typography color="text.secondary">{message}</Typography>
  </Box>
);

export default LoadingSpinner;
