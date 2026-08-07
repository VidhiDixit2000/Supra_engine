import { Alert, AppBar, Box, Container, CssBaseline, Grid, Paper, Stack, Tab, Tabs, ThemeProvider, Toolbar, Typography, createTheme } from '@mui/material';
import { useState } from 'react';
import CandidateTable from '../components/CandidateTable';
import ComparisonView from '../components/ComparisonView';
import DAGView from '../components/DAGView';
import FunnelChart from '../components/FunnelChart';
import LoadingSpinner from '../components/LoadingSpinner';
import PipelineButton from '../components/PipelineButton';
import SummaryCards from '../components/SummaryCards';
import TimingCards from '../components/TimingCards';
import UserSelector from '../components/UserSelector';
import { useUsers } from '../hooks/useUsers';
import { getCandidateSet } from '../services/api';

const theme = createTheme({ palette: { background: { default: '#f6f8fb' }, primary: { main: '#0f5ea8' } }, typography: { fontFamily: ['Inter', 'Roboto', 'Arial', 'sans-serif'].join(',') } });

const Dashboard = () => {
  const { users, selectedUserId, setSelectedUserId, loading: usersLoading, error: usersError } = useUsers();
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [tab, setTab] = useState(0);

  const runPipeline = async () => {
    if (!selectedUserId) return;
    setLoading(true); setError('');
    try { setResult(await getCandidateSet(selectedUserId)); } catch (err) { setError(err.response?.data?.detail || err.message || 'Pipeline request failed.'); } finally { setLoading(false); }
  };

  return (
    <ThemeProvider theme={theme}><CssBaseline /><AppBar position="sticky" elevation={0}><Toolbar><Typography variant="h6" fontWeight={900}>Medi Pipeline Analytics</Typography></Toolbar></AppBar><Container maxWidth="xl" sx={{ py: 4 }}><Stack spacing={3}>
      <Paper elevation={0} sx={{ p: 3, border: '1px solid', borderColor: 'divider', borderRadius: 3 }}><Grid container spacing={2} alignItems="center"><Grid item xs={12} md={8}><Typography variant="h4" fontWeight={900}>Access Candidate Pipeline</Typography><Typography color="text.secondary">Enterprise dashboard for hierarchy reachability, filter funnel, and timing analysis.</Typography></Grid><Grid item xs={12} md={4}><UserSelector users={users} value={selectedUserId} onChange={setSelectedUserId} disabled={usersLoading || loading} /></Grid><Grid item xs={12} md={4}><PipelineButton onClick={runPipeline} loading={loading} disabled={!selectedUserId || usersLoading} /></Grid></Grid></Paper>
      {usersError && <Alert severity="error">{usersError}</Alert>}{error && <Alert severity="error">{error}</Alert>}{loading && <LoadingSpinner message="Running candidate-set pipeline..." />}
      <Tabs value={tab} onChange={(_, value) => setTab(value)}><Tab label="Dashboard" /><Tab label="Comparison" /></Tabs>
      {tab === 0 && <Stack spacing={3}>{result ? <><SummaryCards result={result} /><Grid container spacing={3}><Grid item xs={12} lg={6}><FunnelChart funnel={result.funnel} /></Grid><Grid item xs={12} lg={6}><TimingCards timing={result.pipeline_timing} /></Grid></Grid><CandidateTable candidates={result.candidate_set || []} /><DAGView hierarchy={result.dag || {}} candidates={result.candidate_set || []} entryPoint={result.entry_point} /></> : !loading && <Alert severity="info">Select a user and run the pipeline to view results.</Alert>}</Stack>}
      {tab === 1 && <ComparisonView users={users} />}
    </Stack></Container></ThemeProvider>
  );
};

export default Dashboard;
