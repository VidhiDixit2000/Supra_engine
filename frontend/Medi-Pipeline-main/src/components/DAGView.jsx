import { Box, Card, CardContent, Chip, Typography } from '@mui/material';
import ReactFlow, { Background, Controls, MiniMap, useEdgesState, useNodesState } from 'reactflow';
import { useEffect, useMemo } from 'react';
import 'reactflow/dist/style.css';

const isReachable = (node, candidateIds, entryPoint) => node.reachable === true || candidateIds.has(node.id) || node.id === entryPoint;

const DAGView = ({ hierarchy = {}, candidates = [], entryPoint }) => {
  const candidateIds = useMemo(() => new Set(candidates.map((candidate) => candidate.id)), [candidates]);
  const flowNodes = useMemo(() => (hierarchy.nodes || []).map((node, index) => {
    const reachable = isReachable(node, candidateIds, entryPoint);
    return {
      id: node.id,
      data: { label: node.title || node.label || node.id },
      position: node.position || { x: (index % 6) * 220, y: Math.floor(index / 6) * 130 },
      style: {
        border: node.id === entryPoint ? '3px solid #f59e0b' : '1px solid #94a3b8',
        background: reachable ? '#dcfce7' : '#e5e7eb',
        color: '#0f172a',
        borderRadius: 12,
        padding: 10,
        minWidth: 160,
      },
    };
  }), [candidateIds, entryPoint, hierarchy.nodes]);
  const flowEdges = useMemo(() => (hierarchy.edges || []).map((edge, index) => ({
    id: edge.id || `${edge.source}-${edge.target}-${index}`,
    source: edge.source,
    target: edge.target,
    animated: candidateIds.has(edge.target),
    style: { stroke: candidateIds.has(edge.target) ? '#16a34a' : '#94a3b8' },
  })), [candidateIds, hierarchy.edges]);
  const [nodes, setNodes, onNodesChange] = useNodesState(flowNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(flowEdges);

  useEffect(() => setNodes(flowNodes), [flowNodes, setNodes]);
  useEffect(() => setEdges(flowEdges), [flowEdges, setEdges]);

  return (
    <Card variant="outlined">
      <CardContent>
        <Box alignItems="center" display="flex" gap={1} mb={2} flexWrap="wrap"><Typography variant="h6" fontWeight={800}>Hierarchy DAG</Typography><Chip size="small" label="Green: reachable" color="success" /><Chip size="small" label="Gray: unreachable" /><Chip size="small" label="Gold border: entry point" color="warning" /></Box>
        <Box sx={{ height: { xs: 420, md: 620 }, border: '1px solid', borderColor: 'divider', borderRadius: 2, overflow: 'hidden' }}>
          <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} fitView minZoom={0.1} maxZoom={2}><MiniMap /><Controls /><Background /></ReactFlow>
        </Box>
      </CardContent>
    </Card>
  );
};

export default DAGView;
