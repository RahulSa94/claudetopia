// Creative Intelligence dashboard settings. The page reads only this file for business details,
// so customise here and leave index.html as it is. Fictional example values below.
window.CI_CFG = {
  title: 'Creative Intelligence: Lakeview Homes, Meta',
  currency: '₹',            // symbol shown before money
  locale: 'en-IN',          // number formatting
  // One entry per Meta ad account to analyse. target_cpl = monthly spend target / monthly lead target.
  accounts: [
    {id: '111111111111111', name: 'Riverside', target_cpl: 600},
    {id: '222222222222222', name: 'Hilltop', target_cpl: 1100},
  ],
  default_target_cpl: 1000,
  excluded_note: 'Accounts listed as "never pull" in the profile are excluded.',
  // Extra hook-type rules, checked before the built-in ones: [regex source, label]
  hook_tags: [['influencer|creator', 'Face to camera (influencer)']],
  // Optional paid layer. When false, the page hides the 3-second-view and preview columns' paid notes
  // and video hook falls back to 25% views from Meta's free connector.
  paid_layer: {supermetrics: true},
  // Owners shown on the build cursors (the "who is responsible" layer). Change names freely.
  owners: {patterns: 'Media Manager', briefs: 'Creative Director', disclaimer: 'Legal'},
  // Disclaimer text from your legal team, shown under "How this works". Empty = method notes only.
  disclaimer: '',
};
