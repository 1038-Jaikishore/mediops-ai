import React from 'react';

interface Incident {
  id: string;
  service: string;
  severity: 'high' | 'medium' | 'low';
  status: 'active' | 'resolved' | 'triage';
  message: string;
  timestamp: string;
}

const mockIncidents: Incident[] = [
  {
    id: "INC-9021",
    service: "Laboratory Portal API",
    severity: "high",
    status: "active",
    message: "Postgres database lock detected during bulk test ingestion.",
    timestamp: "2026-07-13 11:04:12"
  },
  {
    id: "INC-9020",
    service: "Appointment Scheduling Service",
    severity: "medium",
    status: "triage",
    message: "Redis cache connection timeout. Fallback to SQL Database.",
    timestamp: "2026-07-13 11:02:40"
  },
  {
    id: "INC-9019",
    service: "Billing & Invoicing Portal",
    severity: "high",
    status: "resolved",
    message: "Payment Gateway returned HTTP 504 gateway timeout.",
    timestamp: "2026-07-13 10:44:50"
  },
  {
    id: "INC-9018",
    service: "Patient Authentication Portal",
    severity: "low",
    status: "resolved",
    message: "Slight auth validation latency spikes during peak shift change.",
    timestamp: "2026-07-13 09:12:15"
  }
];

const IncidentsView: React.FC = () => {
  return (
    <div>
      <div className="dashboard-header">
        <div>
          <h1 className="header-title">Incidents Console</h1>
          <p className="header-subtitle">Track and review automated incident response logs</p>
        </div>
      </div>

      <div className="panel">
        <div className="panel-header">
          <h2 className="panel-title">System Incidents</h2>
        </div>
        <div className="table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>Incident ID</th>
                <th>Affected Service</th>
                <th>Severity</th>
                <th>Status</th>
                <th>Issue Summary</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {mockIncidents.map((inc) => (
                <tr key={inc.id}>
                  <td style={{ fontWeight: 600, color: 'var(--accent-cyan)' }}>{inc.id}</td>
                  <td style={{ fontWeight: 500 }}>{inc.service}</td>
                  <td>
                    <span className={`badge badge-${inc.severity}`}>
                      {inc.severity}
                    </span>
                  </td>
                  <td>
                    <span className={`badge badge-${inc.status}`}>
                      {inc.status}
                    </span>
                  </td>
                  <td style={{ color: 'var(--text-secondary)' }}>{inc.message}</td>
                  <td>{inc.timestamp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default IncidentsView;
