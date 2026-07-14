import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { AppBar, Toolbar, Box, Typography, IconButton, Avatar, Menu, MenuItem } from "@mui/material";
import LogoutIcon from "@mui/icons-material/Logout";
import { logout } from "../../store/slices/authSlice";

export default function Navbar() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const user = useSelector((state) => state.auth.user);
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleLogout = () => {
    dispatch(logout());
    navigate("/login");
  };

  const initials = user?.full_name
    ? user.full_name
        .split(" ")
        .map((p) => p[0])
        .slice(0, 2)
        .join("")
        .toUpperCase()
    : "U";

  return (
    <AppBar
      position="fixed"
      elevation={0}
      sx={{
        width: `calc(100% - 240px)`,
        ml: "240px",
        backgroundColor: "#fff",
        borderBottom: "1px solid #EBEEF5",
        color: "text.primary",
      }}
    >
      <Toolbar sx={{ justifyContent: "space-between" }}>
        <Typography variant="subtitle1" fontWeight={600}>
          AI-First Pharma CRM
        </Typography>
        <Box sx={{ display: "flex", alignItems: "center", gap: 1.5 }}>
          <Typography variant="body2" color="text.secondary">
            {user?.full_name || "Field Rep"}
          </Typography>
          <IconButton onClick={(e) => setAnchorEl(e.currentTarget)} size="small">
            <Avatar sx={{ width: 34, height: 34, bgcolor: "primary.main", fontSize: 14 }}>{initials}</Avatar>
          </IconButton>
          <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={() => setAnchorEl(null)}>
            <MenuItem onClick={handleLogout}>
              <LogoutIcon fontSize="small" sx={{ mr: 1 }} /> Logout
            </MenuItem>
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
}
