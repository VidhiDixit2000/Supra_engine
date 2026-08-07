import { Card, CardContent, Grid, Typography } from '@mui/material';
import { formatMs } from '../utils/formatters';

const timingKeys = [
  ['total_ms', 'Total Time'],
  ['permission_compile_ms', 'Permission Compile'],
  ['bfs_ms', 'BFS'],
  ['zone2_inject_ms', 'Zone2 Injection'],
  ['check1_ms', 'Check 1'],
  ['check2_ms', 'Check 2'],
  ['check3_ms', 'Check 3'],
  ['check4_ms', 'Check 4'],
  ['check5_ms', 'Check 5'],
];

const TimingCards = ({ timing = {} }) => (
  <Grid container spacing={2}>
    {timingKeys.map(([key, label], index) => (
      <Grid item xs={12} sm={6} md={4} lg={index === 0 ? 4 : 2} key={key}>
        <Card variant="outlined" sx={{ height: '100%', bgcolor: index === 0 ? 'primary.50' : 'background.paper' }}>
          <CardContent>
            <Typography color="text.secondary" variant="caption">{label}</Typography>
            <Typography variant={index === 0 ? 'h5' : 'h6'} fontWeight={800}>{formatMs(timing[key])}</Typography>
          </CardContent>
        </Card>
      </Grid>
    ))}
  </Grid>
);

export default TimingCards;
