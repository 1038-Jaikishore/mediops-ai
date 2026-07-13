import React, { useEffect, useState } from 'react';

interface Log {
  timestamp: string;
  level: 'INFO' | 'WARN' | 'ERROR';
  message: string;
}

const mockLogs: Log[] = [
  { timestamp: "11:12:01", level: "INFO", message: "Starting Hospital Operations Simulator server process..." },
  { timestamp: "11:12:02", level: "INFO", message: "Registering endpoints: [/portal, /laboratory, /billing, /pharmacy]" },
  { timestamp: "11:12:05", level: "INFO", message: "Connection pool established to Postgres Cluster." },
  { timestamp: "11:12:06", level: "INFO", message: "Scheduler active: polling Laboratory ingest queue." },
  { timestamp: "11:12:08", level: "WARN", message: "Laboratory Queue latency high (>2.5s)." },
  { timestamp: "11:12:12", level: "ERROR", message: "DB Connection Lock on 'labs_results_pkey': database transaction aborted." },
  { timestamp: "11:12:13", level: "INFO", message: "Root Cause Agent triggered: Analyzing transaction metrics..." },
  { timestamp: "11:12:15", level: "INFO", message: "Triage Agent updated INC-9021 severity to HIGH." },
];

const LogsView: React.FC = () => {
  const [logs, setLogs] = useState<Log[]>(mockLogs);

  useEffect(() => {
    const interval = setInterval(() => {
      const messages = [
        "Authentication check passed for Operator: session active.",
        "Ingested 15 patient vitals records successfully.",
        "Billing sync running: 4 active cycles parsed.",
        "Cache hit ratio stable at 94.2%.",
        "API Gateway refreshed configuration token.",
      ];
      const levels: ('INFO' | 'WARN')[] = ["INFO", "WARN"];
      const randomMessage = messages[Math.floor(Math.random() * messages.length)];
      const randomLevel = levels[Math.floor(Math.random() * levels.length)];
      const now = new Date();
      const timeStr = now.toTimeString().split(' ')[0];

      setLogs((prev) => [...prev.slice(-20), { timestamp: timeStr, level: randomLevel, message: randomMessage }]);
    }, 4000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <div className="dashboard-header">
        <div>
          <h1 className="header-title">Structured Log Stream</h1>
          <p className="header-subtitle">Real-time analytical and operational logs parsed by MediOps AI</p>
        </div>
      </div>

      <div className="panel">
        <div className="panel-header">
          <h2 className="panel-title">Console Stream</h2>
        </div>
        <div className="log-stream">
          {logs.map((log, idx) => (
            <div key={idx} className="log-entry">
              <span className="log-time">[{log.timestamp}]</span>
              <span className={`log-level ${log.level}`}>{log.level}</span>
              <span>{log.message}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default LogsView;
