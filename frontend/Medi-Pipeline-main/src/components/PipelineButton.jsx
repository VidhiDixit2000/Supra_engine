import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import { Button, CircularProgress } from '@mui/material';

const PipelineButton = ({ onClick, loading, disabled }) => (
  <Button
    fullWidth
    size="large"
    variant="contained"
    onClick={onClick}
    disabled={disabled || loading}
    startIcon={loading ? <CircularProgress color="inherit" size={20} /> : <PlayArrowIcon />}
    sx={{ py: 1.8, fontWeight: 800, borderRadius: 2 }}
  >
    {loading ? 'Running Pipeline' : 'Run Pipeline'}
  </Button>
);

export default PipelineButton;
