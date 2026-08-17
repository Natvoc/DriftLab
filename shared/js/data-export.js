// DriftLab shared data schema + export helpers.
// Every experiment MUST use this module instead of reinventing trial
// storage or CSV/JSON export — this is what lets analysis/io.py load any
// task's export without task-specific code.

const REQUIRED_COLUMNS = [
  "participant_id",
  "task",
  "block",
  "trial_index",
  "rt",
  "correct",
  "timestamp",
];

function generateParticipantId() {
  return crypto.randomUUID();
}

class DriftLabDataCollector {
  constructor(taskName) {
    this.taskName = taskName;
    this.participantId = generateParticipantId();
    this.rows = [];
  }

  // rowData: block, trial_index, rt, correct, plus any task-specific
  // extra fields (e.g. word, ink_color, congruency for Stroop). Common
  // fields (participant_id, task, timestamp) are filled in here.
  addTrial(rowData) {
    const row = {
      participant_id: this.participantId,
      task: this.taskName,
      timestamp: new Date().toISOString(),
      ...rowData,
    };

    const missing = REQUIRED_COLUMNS.filter((col) => row[col] === undefined);
    if (missing.length > 0) {
      throw new Error(
        `DriftLabDataCollector: trial is missing required column(s): ${missing.join(", ")}`
      );
    }

    this.rows.push(row);
    return row;
  }

  // Column order: required columns first (stable across tasks), then
  // whatever extra columns each task added, in first-seen order.
  _columnOrder() {
    const extra = [];
    for (const row of this.rows) {
      for (const key of Object.keys(row)) {
        if (!REQUIRED_COLUMNS.includes(key) && !extra.includes(key)) {
          extra.push(key);
        }
      }
    }
    return [...REQUIRED_COLUMNS, ...extra];
  }

  toCSV() {
    const columns = this._columnOrder();
    const escape = (value) => {
      if (value === undefined || value === null) return "";
      const str = String(value);
      if (/[",\n]/.test(str)) {
        return `"${str.replace(/"/g, '""')}"`;
      }
      return str;
    };
    const lines = [columns.join(",")];
    for (const row of this.rows) {
      lines.push(columns.map((col) => escape(row[col])).join(","));
    }
    return lines.join("\n");
  }

  toJSON() {
    return JSON.stringify(this.rows, null, 2);
  }

  _download(content, filename, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }

  downloadCSV(filename = `${this.taskName}_${this.participantId}.csv`) {
    this._download(this.toCSV(), filename, "text/csv");
  }

  downloadJSON(filename = `${this.taskName}_${this.participantId}.json`) {
    this._download(this.toJSON(), filename, "application/json");
  }
}
