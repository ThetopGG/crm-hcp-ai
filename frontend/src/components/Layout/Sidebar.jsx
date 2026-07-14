import React from "react";
import { NavLink } from "react-router-dom";
import { Drawer, List, ListItemButton, ListItemIcon, ListItemText, Toolbar, Box, Typography } from "@mui/material";
import DashboardIcon from "@mui/icons-material/DashboardOutlined";
import PeopleIcon from "@mui/icons-material/PeopleAltOutlined";
import HistoryIcon from "@mui/icons-material/HistoryOutlined";
import EditNoteIcon from "@mui/icons-material/EditNoteOutlined";
import SettingsIcon from "@mui/icons-material/SettingsOutlined";
import MedicalServicesIcon from "@mui/icons-material/MedicalServicesOutlined";

const drawerWidth = 240;

const navItems = [
  { label: "Dashboard", path: "/dashboard", icon: <DashboardIcon /> },
  { label: "HCP List", path: "/hcps", icon: <PeopleIcon /> },
  { label: "Log Interaction", path: "/log-interaction", icon: <EditNoteIcon /> },
  { label: "Interaction History", path: "/history", icon: <HistoryIcon /> },
  { label: "Settings", path: "/settings", icon: <SettingsIcon /> },
];

export default function Sidebar() {
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: {
          width: drawerWidth,
          boxSizing: "border-box",
          borderRight: "1px solid #EBEEF5",
          backgroundColor: "#FFFFFF",
        },
      }}
    >
      <Toolbar sx={{ px: 3, py: 2.5 }}>
        <Box sx={{ display: "flex", alignItems: "center", gap: 1.2 }}>
          <MedicalServicesIcon color="primary" fontSize="medium" />
          <Typography variant="h6" fontWeight={700} color="primary.dark">
            CRM HCP AI
          </Typography>
        </Box>
      </Toolbar>
      <List sx={{ px: 1.5 }}>
        {navItems.map((item) => (
          <ListItemButton
            key={item.path}
            component={NavLink}
            to={item.path}
            sx={{
              borderRadius: 2,
              mb: 0.5,
              "&.active": {
                backgroundColor: "primary.main",
                color: "#fff",
                "& .MuiListItemIcon-root": { color: "#fff" },
              },
            }}
          >
            <ListItemIcon sx={{ minWidth: 38 }}>{item.icon}</ListItemIcon>
            <ListItemText primaryTypographyProps={{ fontWeight: 500 }} primary={item.label} />
          </ListItemButton>
        ))}
      </List>
    </Drawer>
  );
}
