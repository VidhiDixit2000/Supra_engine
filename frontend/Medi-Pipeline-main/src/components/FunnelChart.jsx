import { Box, Card, CardContent, Typography } from '@mui/material';
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

const labels = {
  total_nodes: 'Total Nodes',
  after_bfs: 'After BFS',
  after_zone2: 'After Zone2',
  after_check1: 'Check 1',
  after_check2: 'Check 2',
  after_check3: 'Check 3',
  after_check4: 'Check 4',
  after_check5: 'Check 5',
};

const FunnelChart = ({ funnel = {}, title = 'Filter Funnel' }) => {
  const data = Object.keys(labels).map((key) => ({ stage: labels[key], count: funnel[key] ?? 0 }));
  return (
    <Card variant="outlined" sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" fontWeight={800} gutterBottom>{title}</Typography>
        <Box sx={{ width: '100%', height: 320 }}>
          <ResponsiveContainer>
            <BarChart data={data} margin={{ top: 10, right: 16, left: 0, bottom: 50 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="stage" angle={-35} textAnchor="end" interval={0} height={70} tick={{ fontSize: 12 }} />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="count" fill="#1976d2" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Box>
      </CardContent>
    </Card>
  );
};

export default FunnelChart;
