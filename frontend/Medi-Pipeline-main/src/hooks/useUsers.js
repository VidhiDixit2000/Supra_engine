import { useEffect, useState } from 'react';
import { getUsers } from '../services/api';

export const useUsers = () => {
  const [users, setUsers] = useState([]);
  const [selectedUserId, setSelectedUserId] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;

    const loadUsers = async () => {
      try {
        setLoading(true);
        const data = await getUsers();
        if (!active) return;
        setUsers(Array.isArray(data) ? data : []);
        setSelectedUserId(data?.[0]?.id || '');
        setError('');
      } catch (err) {
        if (!active) return;
        setError(err.response?.data?.detail || err.message || 'Unable to load users.');
      } finally {
        if (active) setLoading(false);
      }
    };

    loadUsers();
    return () => {
      active = false;
    };
  }, []);

  return { users, selectedUserId, setSelectedUserId, loading, error };
};
