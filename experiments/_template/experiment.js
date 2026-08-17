// Copy this folder to experiments/<your-task>/ and:
//   1. Rename the task string below.
//   2. Replace the single demo trial with your real timeline.
//   3. Add extra fields to collector.addTrial() as needed (they don't
//      need to be declared anywhere else — analysis/io.py picks up any
//      column automatically).
//   4. Add an entry to experiments/registry.json.

const TASK_NAME = "template";

const collector = new DriftLabDataCollector(TASK_NAME);

const jsPsych = initJsPsych({
  on_finish: () => {
    showDownloadScreen(collector);
  },
});

const instructions = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: `
    <div class="driftlab-instructions">
      <h2>Template task</h2>
      <p>Press <kbd>A</kbd> when you see the letter A on screen.</p>
      <p>Press any key to start.</p>
    </div>
  `,
};

const fixation = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: '<div class="driftlab-fixation">+</div>',
  choices: "NO_KEYS",
  trial_duration: 500,
};

const trial = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: '<div class="driftlab-stimulus">A</div>',
  choices: ["a"],
  trial_duration: 2000,
  on_finish: (data) => {
    collector.addTrial({
      block: "test",
      // trial_index counts trials within the whole session, not per block —
      // for a real (multi-trial) task, use a counter that keeps
      // incrementing across blocks instead of a literal 0. See
      // experiments/stroop/experiment.js for the pattern.
      trial_index: 0,
      rt: data.rt,
      correct: data.response === "a" ? 1 : 0,
    });
  },
};

function showDownloadScreen(collector) {
  document.body.innerHTML = `
    <main class="driftlab-container">
      <h2>Done — thank you!</h2>
      <p>Download your data:</p>
      <button class="driftlab-btn" id="dl-csv">Download CSV</button>
      <button class="driftlab-btn" id="dl-json">Download JSON</button>
    </main>
  `;
  document.getElementById("dl-csv").addEventListener("click", () => collector.downloadCSV());
  document.getElementById("dl-json").addEventListener("click", () => collector.downloadJSON());
}

jsPsych.run([instructions, fixation, trial]);
