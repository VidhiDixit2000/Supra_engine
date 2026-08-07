import { FormControl, InputLabel, MenuItem, Select, Stack, Typography } from '@mui/material';

const UserSelector = ({ users, value, onChange, disabled = false, label = 'User' }) => (
  <FormControl fullWidth disabled={disabled || users.length === 0}>
    <InputLabel id={`${label}-selector-label`}>{label}</InputLabel>
    <Select
      labelId={`${label}-selector-label`}
      value={value}
      label={label}
      onChange={(event) => onChange(event.target.value)}
    >
      {users.map((user) => (
        <MenuItem key={user.id} value={user.id}>
          <Stack>
            <Typography fontWeight={700}>{user.name}</Typography>
            <Typography variant="caption" color="text.secondary">{user.role} · {user.id}</Typography>
          </Stack>
        </MenuItem>
      ))}
    </Select>
  </FormControl>
);

export default UserSelector;
