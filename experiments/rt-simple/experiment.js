const TASK_NAME = "rt-simple";

const FIXATION_DURATION_MS = 500;
const FOREPERIOD_MIN_MS = 1000;
const FOREPERIOD_MAX_MS = 3000;
const RESPONSE_TIMEOUT_MS = 2000;
const PRACTICE_TRIALS = 5;
const TEST_TRIALS = 30;
const RESPONSE_KEY = " ";

const collector = new DriftLabDataCollector(TASK_NAME);

const jsPsych = initJsPsych({
  on_finish: () => {
    showDownloadScreen(collector);
  },
});

// See DECISIONS.md (2026-08-17, "Gotcha de jsPsych: trial_index colisiona
// con el interno de jsPsych") — never name a custom data field trial_index.
let sessionTrialCounter = 0;

function randomForeperiod() {
  return Math.floor(Math.random() * (FOREPERIOD_MAX_MS - FOREPERIOD_MIN_MS + 1)) + FOREPERIOD_MIN_MS;
}

function buildBlockTrials(count, blockName) {
  const trials = [];
  for (let i = 0; i < count; i++) {
    trials.push({
      type: jsPsychHtmlKeyboardResponse,
      stimulus: '<div class="driftlab-fixation">+</div>',
      choices: "NO_KEYS",
      trial_duration: FIXATION_DURATION_MS,
    });

    // Variable foreperiod (blank screen) so the stimulus onset is
    // unpredictable — discourages anticipatory responses.
    trials.push({
      type: jsPsychHtmlKeyboardResponse,
      stimulus: "",
      choices: "NO_KEYS",
      trial_duration: randomForeperiod,
    });

    trials.push({
      type: jsPsychHtmlKeyboardResponse,
      stimulus: '<div class="driftlab-stimulus">●</div>',
      choices: [RESPONSE_KEY],
      trial_duration: RESPONSE_TIMEOUT_MS,
      data: {
        block: blockName,
        driftlab_trial_index: sessionTrialCounter++,
      },
      on_finish: (data) => {
        data.correct = data.response === RESPONSE_KEY ? 1 : 0;
        collector.addTrial({
          block: data.block,
          trial_index: data.driftlab_trial_index,
          rt: data.rt,
          correct: data.correct,
        });
      },
    });
  }
  return trials;
}

const instructions = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: `
    <div class="driftlab-instructions">
      <h2>Simple reaction time task</h2>
      <p>Watch for the dot (●) to appear, then press <kbd>Space</kbd> as fast as you can.</p>
      <p>You'll start with 5 practice trials, then 30 test trials.</p>
      <p>Press any key to start practice.</p>
    </div>
  `,
};

const practiceTransition = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: `
    <div class="driftlab-instructions">
      <p>Practice done. Now the real test block starts.</p>
      <p>Press any key to continue.</p>
    </div>
  `,
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

const timeline = [
  instructions,
  ...buildBlockTrials(PRACTICE_TRIALS, "practice"),
  practiceTransition,
  ...buildBlockTrials(TEST_TRIALS, "test"),
];

jsPsych.run(timeline);
