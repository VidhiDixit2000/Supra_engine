import { Alert, Box, Button, Card, CardContent, Checkbox, CircularProgress, FormControl, InputLabel, ListItemText, MenuItem, Select, Stack, Typography } from '@mui/material';
import { useState } from 'react';
import { getCandidateSet } from '../services/api';
import FunnelChart from './FunnelChart';
import TimingCards from './TimingCards';
import { formatMs, formatNumber } from '../utils/formatters';

const ComparisonView = ({ users = [] }) => {
  const [selectedIds, setSelectedIds] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState([]);

  const runComparison = async () => {
  setLoading(true);
  setError([]);

  try {
    const responses = await Promise.allSettled(
      selectedIds.map((id) => getCandidateSet(id))
    );

    const successfulResults = responses
      .filter((r) => r.status === "fulfilled")
      .map((r) => r.value);

    const errors = responses
      .filter((r) => r.status === "rejected")
      .map((r) => r.reason.response?.data?.detail || r.reason.message);

    if (errors.length > 0) {
      setResults([]);              // Don't show graphs
      setError(errors); // Show all errors
    } else {
      setResults(successfulResults);
      setError([]);
    }

  } catch (err) {
    // This catch is only for unexpected JS errors
    setResults([]);
    setError(err.message || "Comparison failed.");
  } finally {
    setLoading(false);
  }
};

  return (
    <Stack spacing={3}>
      <Box display="flex" gap={2} flexWrap="wrap" alignItems="center">
        <FormControl sx={{ minWidth: 320, flex: 1 }}><InputLabel>Compare up to 3 users</InputLabel><Select multiple value={selectedIds} label="Compare up to 3 users" renderValue={(ids) => ids.map((id) => users.find((u) => u.id === id)?.name || id).join(', ')} onChange={(event) => setSelectedIds(event.target.value.slice(0, 3))}>{users.map((user) => <MenuItem key={user.id} value={user.id}><Checkbox checked={selectedIds.includes(user.id)} /><ListItemText primary={user.name} secondary={user.role} /></MenuItem>)}</Select></FormControl>
        <Button variant="contained" disabled={loading || selectedIds.length === 0} onClick={runComparison}>{loading ? <CircularProgress size={24} color="inherit" /> : 'Run Comparison'}</Button>
      </Box>
      {error.length > 0 && (
  <Alert severity="error">
    <ul style={{ margin: 0, paddingLeft: "20px" }}>
      {error.map((err, index) => (
        <li key={index}>{err}</li>
      ))}
    </ul>
  </Alert>
)}
      <Box display="grid" gridTemplateColumns={{ xs: '1fr', md: `repeat(${Math.max(results.length, 1)}, minmax(0, 1fr))` }} gap={2}>
        {results.map((result) => <Card variant="outlined" key={result.user}><CardContent><Typography variant="h6" fontWeight={800}>{result.user_name}</Typography><Typography color="text.secondary">{result.role} · {result.entry_point}</Typography><Typography mt={2}>Candidates: <b>{formatNumber(result.candidate_set?.length)}</b></Typography><Typography>Total: <b>{formatMs(result.pipeline_timing?.total_ms)}</b></Typography><Box mt={2}><FunnelChart funnel={result.funnel} title="Funnel" /></Box><Box mt={2}><TimingCards timing={result.pipeline_timing} /></Box></CardContent></Card>)}
      </Box>
    </Stack>
  );
};

export default ComparisonView;
