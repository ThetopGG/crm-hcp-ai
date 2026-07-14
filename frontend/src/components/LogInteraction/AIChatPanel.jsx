import React, { useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Paper, Typography, Box, TextField, IconButton, Avatar, CircularProgress, Chip } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import SmartToyIcon from "@mui/icons-material/SmartToyOutlined";
import PersonIcon from "@mui/icons-material/PersonOutline";
import api from "../../api/axios";
import { addUserMessage, addAssistantMessage, setSending } from "../../store/slices/chatSlice";

export default function AIChatPanel({ onFormExtracted, currentInteractionId }) {
  const dispatch = useDispatch();
  const { messages, isSending } = useSelector((state) => state.chat);
  const [input, setInput] = useState("");
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || isSending) return;

    dispatch(addUserMessage(text));
    setInput("");
    dispatch(setSending(true));

    try {
      const { data } = await api.post("/api/chat/", {
        message: text,
        interaction_id: currentInteractionId || null,
      });

      dispatch(addAssistantMessage(data.reply));

      if (data.extracted_form) {
        onFormExtracted(data.extracted_form, data);
      }
    } catch (err) {
      dispatch(addAssistantMessage("Sorry, something went wrong reaching the AI assistant. Please try again."));
      console.error(err);
    } finally {
      dispatch(setSending(false));
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Paper sx={{ p: 3, height: "100%", display: "flex", flexDirection: "column" }}>
      <Box sx={{ display: "flex", alignItems: "center", gap: 1, mb: 0.5 }}>
        <SmartToyIcon color="secondary" />
        <Typography variant="h6">AI Assistant</Typography>
      </Box>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Describe your meeting naturally — the assistant will summarize it and auto-fill the form.
      </Typography>

      <Box
        sx={{
          flexGrow: 1,
          overflowY: "auto",
          display: "flex",
          flexDirection: "column",
          gap: 1.5,
          mb: 2,
          minHeight: 300,
          maxHeight: 420,
          pr: 0.5,
        }}
      >
        {messages.map((m, idx) => (
          <Box
            key={idx}
            sx={{
              display: "flex",
              gap: 1,
              flexDirection: m.role === "user" ? "row-reverse" : "row",
              alignItems: "flex-start",
            }}
          >
            <Avatar sx={{ width: 28, height: 28, bgcolor: m.role === "user" ? "primary.main" : "secondary.main" }}>
              {m.role === "user" ? <PersonIcon fontSize="small" /> : <SmartToyIcon fontSize="small" />}
            </Avatar>
            <Box
              sx={{
                bgcolor: m.role === "user" ? "primary.main" : "#F1F3F9",
                color: m.role === "user" ? "#fff" : "text.primary",
                px: 1.8,
                py: 1,
                borderRadius: 2,
                maxWidth: "80%",
                whiteSpace: "pre-wrap",
              }}
            >
              <Typography variant="body2">{m.content}</Typography>
            </Box>
          </Box>
        ))}
        {isSending && (
          <Box sx={{ display: "flex", alignItems: "center", gap: 1, pl: 4 }}>
            <CircularProgress size={16} />
            <Typography variant="caption" color="text.secondary">
              Thinking...
            </Typography>
          </Box>
        )}
        <div ref={bottomRef} />
      </Box>

      <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap", mb: 1 }}>
        {["Log a new visit", "Search past visits", "Generate a follow-up email", "Show me insights"].map((s) => (
          <Chip key={s} size="small" label={s} variant="outlined" onClick={() => setInput(s + ": ")} />
        ))}
      </Box>

      <Box sx={{ display: "flex", gap: 1 }}>
        <TextField
          fullWidth
          multiline
          maxRows={4}
          placeholder="e.g. I met Dr Sharma today at Apollo Hospital. We discussed CardX. He wants efficacy data next Monday."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          size="small"
        />
        <IconButton color="primary" onClick={handleSend} disabled={isSending || !input.trim()} sx={{ alignSelf: "flex-end" }}>
          <SendIcon />
        </IconButton>
      </Box>
    </Paper>
  );
}
