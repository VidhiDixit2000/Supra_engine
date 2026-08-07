import { Card, CardContent, Grid, Typography } from '@mui/material';

const items = (result) => [
  ['User Name', result?.user_name],
  ['Role', result?.role],
  ['Ceiling Level', result?.ceiling_level],
  ['Entry Point', result?.entry_point],
];

const SummaryCards = ({ result }) => (
  <Grid container spacing={2}>
    {items(result).map(([label, value]) => (
      <Grid item xs={12} sm={6} md={3} key={label}>
        <Card variant="outlined" sx={{ height: '100%' }}>
          <CardContent>
            <Typography color="text.secondary" variant="overline">{label}</Typography>
            <Typography variant="h6" fontWeight={800} noWrap title={String(value ?? '—')}>{value ?? '—'}</Typography>
          </CardContent>
        </Card>
      </Grid>
    ))}
  </Grid>
);

export default SummaryCards;
