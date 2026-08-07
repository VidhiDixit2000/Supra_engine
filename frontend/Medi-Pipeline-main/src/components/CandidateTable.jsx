import { Box, Dialog, DialogContent, DialogTitle, IconButton, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TableSortLabel, TextField, Typography } from '@mui/material';
import VisibilityIcon from '@mui/icons-material/Visibility';
import { useMemo, useState } from 'react';
import { formatImportance } from '../utils/formatters';

const columns = [
  ['id', 'Node ID'], ['title', 'Title'], ['type', 'Type'], ['department', 'Department'],
  ['zone', 'Zone'], ['importance', 'Importance'], ['distance_from_entry', 'Distance'], ['compression_hint', 'Compression Hint'],
];

const CandidateTable = ({ candidates = [] }) => {
  const [orderBy, setOrderBy] = useState('importance');
  const [order, setOrder] = useState('desc');
  const [query, setQuery] = useState('');
  const [selected, setSelected] = useState(null);

  const sorted = useMemo(() => candidates
    .filter((item) => JSON.stringify(item).toLowerCase().includes(query.toLowerCase()))
    .sort((a, b) => {
      const av = a[orderBy]; const bv = b[orderBy];
      const result = typeof av === 'number' && typeof bv === 'number' ? av - bv : String(av ?? '').localeCompare(String(bv ?? ''));
      return order === 'asc' ? result : -result;
    }), [candidates, orderBy, order, query]);

  const sort = (key) => {
    setOrder((prev) => (orderBy === key && prev === 'asc' ? 'desc' : 'asc'));
    setOrderBy(key);
  };

  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Box alignItems="center" display="flex" flexWrap="wrap" gap={2} justifyContent="space-between" mb={2}>
        <Typography variant="h6" fontWeight={800}>Candidate Set ({sorted.length})</Typography>
        <TextField size="small" label="Search candidates" value={query} onChange={(e) => setQuery(e.target.value)} />
      </Box>
      <TableContainer sx={{ maxHeight: 520 }}>
        <Table stickyHeader size="small">
          <TableHead><TableRow>{columns.map(([key, label]) => <TableCell key={key}><TableSortLabel active={orderBy === key} direction={orderBy === key ? order : 'asc'} onClick={() => sort(key)}>{label}</TableSortLabel></TableCell>)}<TableCell>Content</TableCell></TableRow></TableHead>
          <TableBody>{sorted.map((row) => <TableRow hover key={row.id}><TableCell>{row.id}</TableCell><TableCell>{row.title}</TableCell><TableCell>{row.type}</TableCell><TableCell>{row.department}</TableCell><TableCell>{row.zone}</TableCell><TableCell>{formatImportance(row.importance)}</TableCell><TableCell>{row.distance_from_entry}</TableCell><TableCell>{row.compression_hint}</TableCell><TableCell><IconButton aria-label={`View ${row.id}`} onClick={() => setSelected(row)}><VisibilityIcon /></IconButton></TableCell></TableRow>)}</TableBody>
        </Table>
      </TableContainer>
      <Dialog open={Boolean(selected)} onClose={() => setSelected(null)} fullWidth maxWidth="md"><DialogTitle>{selected?.title}</DialogTitle><DialogContent><Typography whiteSpace="pre-wrap">{selected?.content || 'No content provided.'}</Typography></DialogContent></Dialog>
    </Paper>
  );
};

export default CandidateTable;
