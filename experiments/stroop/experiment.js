const TASK_NAME = "stroop";

// Colors and their key mapping — see README.md for the mnemonic rationale
// (initial letter of the ink color, not the word).
const COLORS = [
  { name: "red", word: "RED", key: "r" },
  { name: "green", word: "GREEN", key: "g" },
  { name: "blue", word: "BLUE", key: "b" },
  { name: "yellow", word: "YELLOW", key: "y" },
];
const KEY_CHOICES = COLORS.map((c) => c.key);

const FIXATION_DURATION_MS = 500;
const RESPONSE_TIMEOUT_MS = 2000;
const FEEDBACK_DURATION_MS = 600;
const PRACTICE_TRIALS_PER_CONGRUENCY = 4; // 8 practice trials total
const TEST_TRIALS_PER_CONGRUENCY = 24; // 48 test trials total

const collector = new DriftLabDataCollector(TASK_NAME);

const jsPsych = initJsPsych({
  on_finish: () => {
    showDownloadScreen(collector);
  },
});

function pickIncongruentColor(wordColor) {
  const options = COLORS.filter((c) => c.name !== wordColor.name);
  return options[Math.floor(Math.random() * options.length)];
}

// Evenly distributes trials across the 4 words (count must be a multiple of 4).
function makeTrialSpecs(count, congruency) {
  const specs = [];
  for (let i = 0; i < count; i++) {
    const word = COLORS[i % COLORS.length];
    const ink = congruency === "congruent" ? word : pickIncongruentColor(word);
    specs.push({ word, ink, congruency });
  }
  return specs;
}

// trial_index counts trials within the whole session (across blocks), per
// the common data schema — not reset per block.
let sessionTrialCounter = 0;

function buildBlockTrials(specs, blockName, withFeedback) {
  const trials = [];
  specs.forEach((spec) => {
    trials.push({
      type: jsPsychHtmlKeyboardResponse,
      stimulus: '<div class="driftlab-fixation">+</div>',
      choices: "NO_KEYS",
      trial_duration: FIXATION_DURATION_MS,
    });

    trials.push({
      type: jsPsychHtmlKeyboardResponse,
      stimulus: `<div class="driftlab-stimulus" style="color: ${spec.ink.name}">${spec.word.word}</div>`,
      choices: KEY_CHOICES,
      trial_duration: RESPONSE_TIMEOUT_MS,
      data: {
        block: blockName,
        // Named driftlab_trial_index, not trial_index: jsPsych auto-injects
        // its OWN "trial_index" into every trial's data (a running count
        // across the whole timeline, including fixation/feedback filler
        // trials) which would silently overwrite ours on merge.
        driftlab_trial_index: sessionTrialCounter++,
        word: spec.word.word,
        ink_color: spec.ink.name,
        congruency: spec.congruency,
        correct_key: spec.ink.key,
      },
      on_finish: (data) => {
        data.correct = data.response === data.correct_key ? 1 : 0;
        collector.addTrial({
          block: data.block,
          trial_index: data.driftlab_trial_index,
          rt: data.rt,
          correct: data.correct,
          word: data.word,
          ink_color: data.ink_color,
          congruency: data.congruency,
        });
      },
    });

    if (withFeedback) {
      trials.push({
        type: jsPsychHtmlKeyboardResponse,
        stimulus: () => {
          const last = jsPsych.data.get().last(1).values()[0];
          return `<div class="driftlab-instructions">${last.correct ? "Correct!" : "Incorrect."}</div>`;
        },
        choices: "NO_KEYS",
        trial_duration: FEEDBACK_DURATION_MS,
      });
    }
  });
  return trials;
}

const instructions = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: `
    <div class="driftlab-instructions">
      <h2>Stroop task</h2>
      <p>You'll see color words printed in colored ink. Respond to the
      <strong>ink color</strong>, not the word itself.</p>
      <ul>
        <li>Ink is <strong style="color: red">red</strong> → press <kbd>R</kbd></li>
        <li>Ink is <strong style="color: green">green</strong> → press <kbd>G</kbd></li>
        <li>Ink is <strong style="color: blue">blue</strong> → press <kbd>B</kbd></li>
        <li>Ink is <strong style="color: yellow">yellow</strong> → press <kbd>Y</kbd></li>
      </ul>
      <p>You'll start with a short practice block with feedback, then the real test block.</p>
      <p>Press any key to start practice.</p>
    </div>
  `,
};

const practiceTransition = {
  type: jsPsychHtmlKeyboardResponse,
  stimulus: `
    <div class="driftlab-instructions">
      <p>Practice done. Now the real test block starts — same rules, no feedback this time.</p>
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

const practiceSpecs = jsPsych.randomization.shuffle([
  ...makeTrialSpecs(PRACTICE_TRIALS_PER_CONGRUENCY, "congruent"),
  ...makeTrialSpecs(PRACTICE_TRIALS_PER_CONGRUENCY, "incongruent"),
]);
const testSpecs = jsPsych.randomization.shuffle([
  ...makeTrialSpecs(TEST_TRIALS_PER_CONGRUENCY, "congruent"),
  ...makeTrialSpecs(TEST_TRIALS_PER_CONGRUENCY, "incongruent"),
]);

const timeline = [
  instructions,
  ...buildBlockTrials(practiceSpecs, "practice", true),
  practiceTransition,
  ...buildBlockTrials(testSpecs, "test", false),
];

jsPsych.run(timeline);
