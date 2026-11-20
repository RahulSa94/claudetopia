#!/usr/bin/env python3
"""Build the Creative Intelligence dashboard documents from a profile.

Usage: python3 build_dashboard.py profile.json out_dir
profile.json:
{
  "title": "Creative Intelligence: Lakeview Homes, Meta",
  "currency": "₹", "locale": "en-IN",
  "accounts": [{"id": "111111111111111", "name": "Riverside", "target_cpl": 600}],
  "default_target_cpl": 1000,
  "excluded_note": "...", "hook_tags": [["regex", "label"]],
  "paid_layer": {"supermetrics": false},
  "owners": {"patterns": "Media Manager", "briefs": "Creative Director", "disclaimer": "Legal"},
  "disclaimer": "",
  "has_snapshot": false
}
Writes ops_1.json (meta, params, datasets) and ops_2.json (config.js + index.html), each a list of
db_write ops for the Data (dashboard) artifact type. Send each file as one db_write call.
"""
import json, sys, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
prof = json.load(open(sys.argv[1]))
out = sys.argv[2] if len(sys.argv) > 2 else '.'
os.makedirs(out, exist_ok=True)
ids = [str(a['id']).replace('act_', '') for a in prof['accounts']]
today = datetime.date.today()
until = today - datetime.timedelta(days=1)
since = until - datetime.timedelta(days=89)
DATE = '^20[0-9]{2}-[01][0-9]-[0-3][0-9]$'
RULES = {'account': {'description': 'One of the ad accounts in the settings', 'enum': ids},
         'since': {'description': 'A start date', 'pattern': DATE}, 'until': {'description': 'An end date', 'pattern': DATE}}
RANGE = {'description': 'The applied date range', 'pattern': '^\\{"since":"20[0-9]{2}-[01][0-9]-[0-3][0-9]","until":"20[0-9]{2}-[01][0-9]-[0-3][0-9]"\\}$'}
CURSOR = {'description': 'A paging cursor Meta returned', 'pattern': '^[A-Za-z0-9_=-]{1,1000}$'}
CID = 'CIdash' + ''.join(c for c in ids[0] if c.isdigit())[-14:].rjust(14, '0')
AD_FIELDS = ['name', 'adset_id', 'campaign_id', 'objective', 'effective_status', 'amount_spent', 'impressions', 'reach', 'frequency', 'link_click',
             'landing_page_view', 'lead', 'video_play_actions', 'video_p25_watched_actions', 'video_p75_watched_actions', 'video_thruplay_watched_actions']
SET_FIELDS = ['name', 'optimization_goal', 'amount_spent']

def meta_args(level, fields, time_range, cursor=None):
    a = {'ad_account_id': '{{account}}', 'advertiser_job': 'creative_insights_and_ideas', 'client_conversation_id': CID, 'fields': fields,
         'filtering': [{'field': 'amount_spent', 'operator': 'GREATER_THAN', 'value': ['0']}], 'include_additional_context': False,
         'level': level, 'limit': 500, 'reporting_purpose': ['creative'], 'scheduled_task_run': False, 'time_range': time_range}
    if cursor: a['cursor'] = cursor
    return a

TR = '{"since":"{{since}}","until":"{{until}}"}'
ds = {
  'ads': {'title': 'Meta ads for the chosen project and dates', 'description': 'Every ad with spend in the applied dates, from Meta\'s free Ads MCP.',
          'source': {'kind': 'call', 'connector': 'metamcp', 'tool': 'ads_get_ad_entities', 'args': meta_args('ad', AD_FIELDS, TR), 'rules': RULES}},
  'adsets': {'title': 'Meta ad sets and their goals', 'description': 'Every ad set with spend, with its optimisation goal, to split ads by goal and check spend.',
             'source': {'kind': 'call', 'connector': 'metamcp', 'tool': 'ads_get_ad_entities', 'args': meta_args('adset', SET_FIELDS, TR), 'rules': RULES}},
  'ads_page': {'title': 'Meta ads, next page', 'description': 'The next page of ads when there are more than 500; the ads loader asks for it.',
               'source': {'kind': 'call', 'connector': 'metamcp', 'tool': 'ads_get_ad_entities', 'args': meta_args('ad', AD_FIELDS, '{{range}}', '{{cursor}}'),
                          'rules': {'account': RULES['account'], 'range': RANGE, 'cursor': CURSOR}}},
  'adsets_page': {'title': 'Meta ad sets, next page', 'description': 'The next page of ad sets when there are more than 500.',
                  'source': {'kind': 'call', 'connector': 'metamcp', 'tool': 'ads_get_ad_entities', 'args': meta_args('adset', SET_FIELDS, '{{range}}', '{{cursor}}'),
                             'rules': {'account': RULES['account'], 'range': RANGE, 'cursor': CURSOR}}},
}
if prof.get('paid_layer', {}).get('supermetrics'):
    def sm(title, desc, fields):
        return {'title': title + ' (paid layer: Supermetrics)', 'description': desc,
                'source': {'kind': 'call', 'connector': 'Supermetrics', 'tool': 'data_query',
                           'args': {'ds_id': 'FA', 'ds_accounts': '{{account}}', 'fields': fields, 'date_range_type': 'custom', 'start_date': '{{since}}', 'end_date': '{{until}}',
                                    'settings': {'exclude_zero_impressions': True}, 'compress': False, 'max_rows': 3000}, 'rules': RULES}}
    ds['sm_previews'] = sm('Live ad previews', 'Meta ad preview links per ad. Signed links that expire.', 'ad_id,ad_name,desktop_feed_preview_url,mobile_feed_preview_url,instagram_preview_url')
    ds['sm_format'] = sm('Creative type and 3-second views', 'Creative object type and three-second video views per ad.', 'ad_id,ad_name,creative_object_type,action_video_view')
    ds['sm_carousel'] = sm('Carousel cards', 'Ads with carousel cards, one row per card image.', 'ad_id,ad_name,carousel_card_image_url')
    ds['sm_poll'] = {'title': 'Supermetrics result fetch (paid layer)', 'description': 'Fetches a finished Supermetrics query by schedule id.',
                     'source': {'kind': 'call', 'connector': 'Supermetrics', 'tool': 'get_async_query_results', 'args': {'schedule_id': '{{sid}}', 'compress': False},
                                'rules': {'sid': {'description': 'A Supermetrics schedule id', 'pattern': '^[0-9a-f]{64}$'}}}}

ops1 = [{'op': 'set', 'path': 'dash/meta', 'data': {'title': prof.get('title', 'Creative Intelligence')}},
        {'op': 'set', 'path': 'dash/params', 'data': {'account': ids[0], 'since': since.isoformat(), 'until': until.isoformat(), 'goal': '', 'verdict': '', 'format': '',
                                                       'src': 'latest' if prof.get('has_snapshot') else 'live'}}]
ops1 += [{'op': 'set', 'path': 'datasets/' + k, 'data': v} for k, v in ds.items()]
cfg = {k: prof.get(k) for k in ['title', 'currency', 'locale', 'accounts', 'default_target_cpl', 'excluded_note', 'hook_tags', 'paid_layer', 'owners', 'disclaimer'] if k in prof}
config_js = '// Creative Intelligence dashboard settings. Edit this file to customise; leave index.html as it is.\nwindow.CI_CFG = ' + json.dumps(cfg, ensure_ascii=False, indent=2) + ';\n'
ops2 = [{'op': 'set', 'path': 'files/config.js', 'data': {'text': config_js}},
        {'op': 'set', 'path': 'files/index.html', 'data': {'text': open(os.path.join(HERE, 'index.html'), encoding='utf-8').read()}}]
json.dump(ops1, open(os.path.join(out, 'ops_1.json'), 'w'), ensure_ascii=False)
json.dump(ops2, open(os.path.join(out, 'ops_2.json'), 'w'), ensure_ascii=False)
print('ops_1.json', len(ops1), 'ops; ops_2.json', os.path.getsize(os.path.join(out, 'ops_2.json')), 'bytes')
