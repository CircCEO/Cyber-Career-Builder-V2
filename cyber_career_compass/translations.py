"""
Full multi-language support: English, 日本語 (Japanese), 繁體中文 (Traditional Chinese).
All UI strings and question/choice texts keyed by language for instant reload on toggle.
"""

from typing import Dict, List, Any, Optional

# Language codes and sidebar display names
SUPPORTED_LANGUAGES: List[str] = ["en", "ja", "zh_tw"]
LANGUAGE_LABELS: Dict[str, str] = {
    "en": "English",
    "ja": "日本語 (Japanese)",
    "zh_tw": "繁體中文 (Traditional Chinese)",
}

# ─── UI strings (headers, buttons, sidebar, result section) ────────────────────
def _ui_en() -> Dict[str, str]:
    return {
        "app_title": "Cyber Career Simulator",
        "system_init": "System Initialization",
        "mode_select_title": "Select Mission Profile",
        "mode_explorer": "The Explorer (Foundational)",
        "mode_explorer_desc": "A 20-question intro to find your Cyber Archetype. Best for newcomers.",
        "mode_specialist": "The Specialist (Elite)",
        "mode_specialist_desc": "50 Questions. Full NIST TKS Gap Analysis.",
        "mode_operator": "The Operator (Tier 1)",
        "mode_operator_desc": "High-Fidelity Mission Simulator. Branching 2026 scenarios (AI / Supply Chain). Assesses readiness for Critical Infrastructure Protection (ICS/SCADA) and Ransomware Mitigation.",
        "start_explorer": "Enter Explorer",
        "start_specialist": "Enter Specialist",
        "start_operator": "Enter Operator",
        "back_to_hub": "Back to Mission Hub",
        "mission_hub_title": "Mission Hub",
        "nav_mission_hub": "Mission Hub",
        "nav_proving_ground": "The Proving Grounds",
        "pg_reflex_hygiene": "Reflex: Hygiene",
        "pg_validation_nice": "Validation: NICE",
        "pg_livefire_breach": "Live-Fire: Breach",
        "pg_reflex_desc": "10 NIST-mapped threats. Immediate defensive muscle memory.",
        "nav_archetype": "Cyber Archetype",
        "tactical_hub_title": "Tactical Mission Hub",
        "status_ready": "STATUS: READY",
        "system_status_nominal": "SYSTEM STATUS: NOMINAL",
        "vector_id_explorer": "VECTOR_ID: EXP-20",
        "vector_id_specialist": "VECTOR_ID: TKS-50",
        "vector_id_operator": "VECTOR_ID: OP-12",
        "threat_model": "THREAT_MODEL: 2026_STANDARD",
        "op_directive_explorer": "Operational Directive: Assess foundational alignment with NICE work roles. 20-item profile.",
        "op_directive_specialist": "Operational Directive: Full TKS assessment against NIST 2026 framework. 50-item gap analysis.",
        "op_directive_operator": "Operational Directive: Scenario-based mission simulation. 12 missions aligned to 2026 framework.",
        "tlevel_yellow": "T-LEVEL: YELLOW",
        "tlevel_orange": "T-LEVEL: ORANGE",
        "tlevel_red": "T-LEVEL: RED",
        "mission_start": "Mission Start",
        "restart_mission": "Restart Mission",
        "view_dossier": "View Dossier",
        "resume_mission": "Resume Mission",
        "capability_gap_title": "Capability Gap Detected",
        "capability_gap_message": "You have not met the baseline for specialized roles. Complete more missions to build your NICE profile.",
        "suggest_explorer_path": "We suggest the Explorer path for foundational upskilling.",
        "live_biometric_title": "Live Biometric",
        "high_security_dossier_title": "High-Security Dossier",
        "skill_gap_radar_title": "Skill Gap Radar (You vs Professional Baseline)",
        "roadmap_title": "Professional Development Roadmap",
        "ares_node_map_title": "Mission Node Map",
        "ares_deployments_title": "Recommended Training Deployments",
        "ares_guide_ref": "Battle Room descriptions (BR1, BR8, etc.) from Project Ares NIST NICE Guide, Page 47.",
        "ares_top_category_title": "Recommended for your top category",
        "ares_top_category_caption": "Training aligned with your strongest NIST category.",
        "ares_battle_room": "Battle Room",
        "ares_mission": "Mission",
        "ares_learning_path": "Learning Path",
        "ares_training_value": "Training Value",
        "gap_identification_title": "Top 3 NIST K/S Gaps",
        "credential_mapping_title": "Credential Mapping",
        "path_to_readiness_title": "Path to Readiness",
        "path_legend_you": "You",
        "path_legend_gap": "Gap to Elite",
        "radar_legend_baseline": "Professional baseline",
        "mentor_insight_title": "Mentor Insight",
        "mentor_step_1": "Participate in more Blue Team CTFs to build incident response muscle memory.",
        "mentor_step_2": "Study one NIST K/S area per month using NICE Framework task statements.",
        "mentor_step_3": "Shadow or pair with a practitioner in your weakest category for 2–4 weeks.",
        "download_dossier": "Download PDF",
        "resume_explorer": "Resume Explorer",
        "resume_specialist": "Resume Specialist",
        "resume_operator": "Resume Operator",
        "resume_from": "Resume from question",
        "phase_operator": "Mission Scenario",
        "status_operator": "Operator — Mission",
        "operator_results_title": "Mission Complete",
        "welcome_subtitle": "NIST NICE–driven assessment: **Instinct**, **Technical**, and **Deep-Scenario** questions → **Career Dossier** with 7-category radar and certification roadmap.",
        "start_btn": "Start assessment",
        "phase_explorer_instinct": "Instinct (Personality)",
        "phase_explorer_foundations": "NIST Foundations",
        "status_explorer_instinct": "Explorer — Instinct",
        "status_explorer_foundations": "Explorer — Foundations",
        "explorer_results_title": "Your Cyber Archetype",
        "archetype_await_telemetry": "Complete Proving Grounds (10 NIST-mapped questions) to unlock your Cyber Archetype report.",
        "specialist_results_title": "Specialist Dossier",
        "nist_role_id": "NIST Work Role ID",
        "salary_roadmap_2026": "2026 Salary & Certification Roadmap",
        "salary_range": "Typical salary range (2026):",
        "cert_roadmap": "Certification path:",
        "phase_instinct": "Instinct (Personality)",
        "phase_technical": "Technical (Triage)",
        "phase_deep": "Deep Scenario (2026+ trends)",
        "phase_tks": "TKS Gap (2026 NIST)",
        "status_idle": "Idle",
        "status_phase1": "Phase 1 — Instinct",
        "status_phase2": "Phase 2 — Technical",
        "status_phase3": "Phase 3 — Deep Scenario",
        "status_phase4": "Phase 4 — TKS",
        "status_complete": "Complete",
        "question_label": "Choose one:",
        "submit_btn": "Submit",
        "results_title": "Assessment complete",
        "work_role": "Work Role",
        "your_strengths": "Your strengths",
        "category_fit": "NICE Category Fit (7 categories)",
        "role_probability": "Role Probability",
        "recommended_roadmap": "Recommended Roadmap",
        "download_pdf": "Download as PDF",
        "align_success": "Align your path with the NICE Framework.",
        "start_over": "Start over",
        "sidebar_title": "Agent Status",
        "sidebar_status": "Status",
        "sidebar_question": "Question",
        "sidebar_progress": "Progress",
        "sidebar_footer": "NIST NICE Framework · Cyber Career Compass",
        "answered": "answered",
        "of": "of",
        "please_choose": "Please choose an option before submitting.",
        "skill_heatmap_title": "Skill Heatmap",
        "install_fpdf2": "Install fpdf2 for PDF download: pip install fpdf2",
        "pdf_title": "NICE Career Dossier",
        "pdf_work_role": "Work Role",
        "pdf_category": "Category",
        "pdf_strengths": "Your Strengths",
        "pdf_category_profile": "Category Profile (normalized 0-100)",
        "pdf_certs": "Recommended Certifications",
        "language_label": "Language",
        "archetype_builder": "Builder",
        "archetype_builder_desc": "You design and build secure systems. You excel at architecture, secure development, and resilient infrastructure.",
        "archetype_guardian": "Guardian",
        "archetype_guardian_desc": "You protect and defend. You thrive in SOCs, incident response, and real-time threat containment.",
        "archetype_investigator": "Investigator",
        "archetype_investigator_desc": "You analyze and investigate. You connect dots in data, produce intelligence, and build cases.",
        "archetype_operator": "Operator",
        "archetype_operator_desc": "You operate and maintain. You keep systems secure through operations, monitoring, and continuous compliance.",
        "archetype_governor": "Governor",
        "archetype_governor_desc": "You oversee and govern. You align security with strategy, risk, and regulatory requirements.",
        "reflex_system_health_label": "SYSTEM HEALTH",
        "reflex_system_nominal": "System Nominal",
        "reflex_complete_btn": "Complete drill",
        "reflex_neutralize": "NEUTRALIZE",
        "reflex_drop": "DROP",
        "reflex_freeze": "FREEZE",
        "reflex_incorrect_try": "Incorrect.",
        "pg_scores_synced": "Scores synced to C3S radar. Your NICE alignment has been updated.",
    }


def _ui_ja() -> Dict[str, str]:
    return {
        "app_title": "Cyber Career Simulator",
        "system_init": "システム初期化",
        "mode_select_title": "ミッションタイプを選択",
        "mode_explorer": "エクスプローラー（基礎）",
        "mode_explorer_desc": "20問であなたのサイバーアーキタイプを診断。初心者向け。",
        "mode_specialist": "スペシャリスト（上級）",
        "mode_specialist_desc": "50問。NIST TKS ギャップ分析フル版。",
        "mode_operator": "オペレーター (Tier 1)",
        "mode_operator_desc": "高忠実度ミッションシミュレーター。2026年分岐シナリオ（AI・サプライチェーン）。重要インフラ保護（ICS/SCADA）とランサムウェア対策の準備度を評価。",
        "start_explorer": "エクスプローラーを開始",
        "start_specialist": "スペシャリストを開始",
        "start_operator": "オペレーターを開始",
        "back_to_hub": "ミッション Hub に戻る",
        "mission_hub_title": "ミッション Hub",
        "nav_mission_hub": "ミッション Hub",
        "nav_proving_ground": "試練の場",
        "pg_reflex_hygiene": "Reflex: Hygiene",
        "pg_validation_nice": "Validation: NICE",
        "pg_livefire_breach": "Live-Fire: Breach",
        "pg_reflex_desc": "10件のNIST対応脅威。即応防御の筋力メモリ。",
        "nav_archetype": "サイバーアーキタイプ",
        "tactical_hub_title": "戦術ミッション Hub",
        "status_ready": "STATUS: READY",
        "system_status_nominal": "システム状態: 正常",
        "vector_id_explorer": "VECTOR_ID: EXP-20",
        "vector_id_specialist": "VECTOR_ID: TKS-50",
        "vector_id_operator": "VECTOR_ID: OP-12",
        "threat_model": "脅威モデル: 2026_STANDARD",
        "op_directive_explorer": "作戦指針: NICE ワークロールとの基礎的整合性を評価。20項目プロファイル。",
        "op_directive_specialist": "作戦指針: NIST 2026 フレームワークに基づく TKS 総合評価。50項目ギャップ分析。",
        "op_directive_operator": "作戦指針: シナリオベースのミッションシミュレーション。2026年フレームワークに沿った12ミッション。",
        "tlevel_yellow": "T-LEVEL: YELLOW",
        "tlevel_orange": "T-LEVEL: ORANGE",
        "tlevel_red": "T-LEVEL: RED",
        "mission_start": "ミッション開始",
        "restart_mission": "ミッション再開",
        "view_dossier": "Dossier を表示",
        "resume_mission": "ミッションを再開",
        "capability_gap_title": "能力ギャップ検出",
        "capability_gap_message": "専門ロールの基準を満たしていません。NICE プロファイルを構築するためミッションを完了してください。",
        "suggest_explorer_path": "基礎スキルアップにはエクスプローラーパスを推奨します。",
        "live_biometric_title": "ライブバイオメトリクス",
        "high_security_dossier_title": "高セキュリティ Dossier",
        "skill_gap_radar_title": "スキルギャップレーダー（あなた vs プロ基準）",
        "roadmap_title": "プロフェッショナル開発ロードマップ",
        "ares_node_map_title": "ミッションノードマップ",
        "ares_deployments_title": "推奨トレーニング配備",
        "ares_top_category_title": "トップカテゴリ向け推奨",
        "ares_top_category_caption": "最も得意なNISTカテゴリに沿ったトレーニング。",
        "ares_battle_room": "バトルルーム",
        "ares_mission": "ミッション",
        "ares_learning_path": "ラーニングパス",
        "ares_training_value": "トレーニング価値",
        "gap_identification_title": "上位3 NIST K/S ギャップ",
        "credential_mapping_title": "資格マッピング",
        "path_to_readiness_title": "リーディネスへのパス",
        "path_legend_you": "あなた",
        "path_legend_gap": "エリートとの差",
        "radar_legend_baseline": "プロフェッショナル基準",
        "mentor_insight_title": "メンターインサイト",
        "mentor_step_1": "ブルーチームCTFに多く参加し、インシデント対応の筋肉記憶を養いましょう。",
        "mentor_step_2": "NICEフレームワークのタスクステートメントで月1つのNIST K/S領域を学習しましょう。",
        "mentor_step_3": "最も弱いカテゴリで実務者と2〜4週間ペアまたはシャドウしましょう。",
        "download_dossier": "PDF ダウンロード",
        "resume_explorer": "エクスプローラーを再開",
        "resume_specialist": "スペシャリストを再開",
        "resume_operator": "オペレーターを再開",
        "resume_from": "質問から再開",
        "phase_operator": "ミッションシナリオ",
        "status_operator": "オペレーター — ミッション",
        "operator_results_title": "ミッション完了",
        "welcome_subtitle": "NIST NICEに基づくアセスメント：**インスティンクト**・**技術**・**ディープシナリオ**の質問に答えて、7カテゴリレーダーと認定ロードマップ付きの**キャリア Dossier**を取得します。",
        "start_btn": "アセスメントを開始",
        "phase_explorer_instinct": "インスティンクト（性格）",
        "phase_explorer_foundations": "NIST基礎",
        "status_explorer_instinct": "エクスプローラー — インスティンクト",
        "status_explorer_foundations": "エクスプローラー — 基礎",
        "explorer_results_title": "あなたのサイバーアーキタイプ",
        "archetype_await_telemetry": "証明グラウンド（NIST対応10問）を完了すると、サイバーアーキタイプレポートが表示されます。",
        "specialist_results_title": "スペシャリスト Dossier",
        "nist_role_id": "NIST ワークロール ID",
        "salary_roadmap_2026": "2026年 年収・認定ロードマップ",
        "salary_range": "想定年収レンジ（2026年）：",
        "cert_roadmap": "認定パス：",
        "phase_instinct": "インスティンクト（性格）",
        "phase_technical": "技術（トリアージ）",
        "phase_deep": "ディープシナリオ（2026年以降のトレンド）",
        "status_idle": "待機中",
        "status_phase1": "フェーズ1 — インスティンクト",
        "status_phase2": "フェーズ2 — 技術",
        "status_phase3": "フェーズ3 — ディープシナリオ",
        "phase_tks": "TKSギャップ（2026 NIST）",
        "status_phase4": "フェーズ4 — TKS",
        "status_complete": "完了",
        "question_label": "1つ選んでください：",
        "submit_btn": "送信",
        "results_title": "アセスメント完了",
        "work_role": "ワークロール",
        "your_strengths": "あなたの強み",
        "category_fit": "NICEカテゴリ適合（7カテゴリ）",
        "role_probability": "ロール確率",
        "recommended_roadmap": "推奨ロードマップ",
        "download_pdf": "PDFでダウンロード",
        "align_success": "NICEフレームワークに沿ってキャリアを組み立てましょう。",
        "start_over": "最初から",
        "sidebar_title": "エージェントステータス",
        "sidebar_status": "ステータス",
        "sidebar_question": "質問",
        "sidebar_progress": "進捗",
        "sidebar_footer": "NIST NICE Framework · Cyber Career Compass",
        "answered": "回答済み",
        "of": "／",
        "please_choose": "送信前に選択してください。",
        "skill_heatmap_title": "スキルヒートマップ",
        "install_fpdf2": "PDFダウンロードには fpdf2 をインストール: pip install fpdf2",
        "pdf_title": "NICE キャリア Dossier",
        "pdf_work_role": "ワークロール",
        "pdf_category": "カテゴリ",
        "pdf_strengths": "あなたの強み",
        "pdf_category_profile": "カテゴリプロファイル（0-100正規化）",
        "pdf_certs": "推奨認定",
        "language_label": "言語",
        "archetype_builder": "ビルダー",
        "archetype_builder_desc": "セキュアなシステムを設計・構築。アーキテクチャ、セキュア開発、耐障害インフラが得意。",
        "archetype_guardian": "ガーディアン",
        "archetype_guardian_desc": "保護・防御。SOC、インシデント対応、リアルタイム脅威封じ込めで力を発揮。",
        "archetype_investigator": "インベスティゲーター",
        "archetype_investigator_desc": "分析・調査。データからパターンを見つけ、インテリジェンスを産出し、ケースを組み立てる。",
        "archetype_operator": "オペレーター",
        "archetype_operator_desc": "運用・維持。オペレーション、監視、継続的コンプライアンスでシステムを守る。",
        "archetype_governor": "ガバナー",
        "archetype_governor_desc": "監督・統治。セキュリティを戦略・リスク・規制と整合させる。",
        "reflex_system_health_label": "システムヘルス",
        "reflex_system_nominal": "システム正常",
        "reflex_complete_btn": "ドリル完了",
        "reflex_neutralize": "無力化",
        "reflex_drop": "ドロップ",
        "reflex_freeze": "凍結",
        "reflex_incorrect_try": "不正解。",
        "pg_scores_synced": "スコアをC3Sレーダーに同期しました。NICE整合が更新されました。",
    }


def _ui_zh_tw() -> Dict[str, str]:
    return {
        "app_title": "Cyber Career Simulator",
        "system_init": "系統初始化",
        "mode_select_title": "選擇任務類型",
        "mode_explorer": "探索者（基礎）",
        "mode_explorer_desc": "20 題快速找出您的資安原型。適合新手。",
        "mode_specialist": "專家（進階）",
        "mode_specialist_desc": "50 題。完整 NIST TKS 缺口分析。",
        "mode_operator": "維運者 (Tier 1)",
        "mode_operator_desc": "高擬真任務模擬器。2026 分支情境（AI／供應鏈）。評估關鍵基礎設施防護（ICS/SCADA）與勒索軟體緩解之準備度。",
        "start_explorer": "進入探索者",
        "start_specialist": "進入專家",
        "start_operator": "進入維運者",
        "back_to_hub": "返回任務中心",
        "mission_hub_title": "任務中心",
        "nav_mission_hub": "任務中心",
        "nav_proving_ground": "試煉場",
        "pg_reflex_hygiene": "Reflex: Hygiene",
        "pg_validation_nice": "Validation: NICE",
        "pg_livefire_breach": "Live-Fire: Breach",
        "pg_reflex_desc": "10 個 NIST 對應威脅，即時防禦肌肉記憶。",
        "nav_archetype": "網路原型",
        "tactical_hub_title": "戰術任務中心",
        "status_ready": "STATUS: READY",
        "system_status_nominal": "系統狀態: 正常",
        "vector_id_explorer": "VECTOR_ID: EXP-20",
        "vector_id_specialist": "VECTOR_ID: TKS-50",
        "vector_id_operator": "VECTOR_ID: OP-12",
        "threat_model": "威脅模型: 2026_STANDARD",
        "op_directive_explorer": "作戰指示：評估與 NICE 工作角色的基礎對齊。20 題側寫。",
        "op_directive_specialist": "作戰指示：依 NIST 2026 架構進行完整 TKS 評估。50 題缺口分析。",
        "op_directive_operator": "作戰指示：情境式任務模擬。12 個對齊 2026 架構的任務。",
        "tlevel_yellow": "T-LEVEL: YELLOW",
        "tlevel_orange": "T-LEVEL: ORANGE",
        "tlevel_red": "T-LEVEL: RED",
        "mission_start": "開始任務",
        "restart_mission": "重新開始任務",
        "view_dossier": "檢視 Dossier",
        "resume_mission": "繼續任務",
        "capability_gap_title": "偵測到能力落差",
        "capability_gap_message": "尚未達到專業角色的基準。請完成更多任務以建立您的 NICE 側寫。",
        "suggest_explorer_path": "建議使用探索者路徑進行基礎技能提升。",
        "live_biometric_title": "即時生物辨識",
        "high_security_dossier_title": "高安全 Dossier",
        "skill_gap_radar_title": "技能差距雷達（您 vs 專業基準）",
        "roadmap_title": "專業發展路線圖",
        "ares_node_map_title": "任務節點地圖",
        "ares_deployments_title": "推薦訓練部署",
        "ares_top_category_title": "依您最高分類推薦",
        "ares_top_category_caption": "依您最強的NIST分類對齊的訓練。",
        "ares_battle_room": "戰室",
        "ares_mission": "任務",
        "ares_learning_path": "學習路徑",
        "ares_training_value": "訓練價值",
        "gap_identification_title": "前 3 項 NIST K/S 差距",
        "credential_mapping_title": "證照對應",
        "path_to_readiness_title": "就緒度路徑",
        "path_legend_you": "您",
        "path_legend_gap": "與菁英差距",
        "radar_legend_baseline": "專業基準",
        "mentor_insight_title": "導師建議",
        "mentor_step_1": "多參與藍隊 CTF，建立事件應變的熟練度。",
        "mentor_step_2": "每月依 NICE 架構任務敘述專攻一項 NIST K/S 領域。",
        "mentor_step_3": "在最弱類別與從業者配對或見習 2–4 週。",
        "download_dossier": "下載 PDF",
        "resume_explorer": "繼續探索者",
        "resume_specialist": "繼續專家",
        "resume_operator": "繼續維運者",
        "resume_from": "從第",
        "phase_operator": "任務情境",
        "status_operator": "維運者 — 任務",
        "operator_results_title": "任務完成",
        "welcome_subtitle": "以 NIST NICE 為基礎的評估：回答**直覺**、**技術**與**深度情境**題目，取得含 7 類別雷達圖與認證路線圖的**職涯 Dossier**。",
        "start_btn": "開始評估",
        "phase_explorer_instinct": "直覺（性格）",
        "phase_explorer_foundations": "NIST 基礎",
        "status_explorer_instinct": "探索者 — 直覺",
        "status_explorer_foundations": "探索者 — 基礎",
        "explorer_results_title": "您的資安原型",
        "archetype_await_telemetry": "完成試煉場（10 題 NIST 對應題）即可解鎖您的資安原型報告。",
        "specialist_results_title": "專家 Dossier",
        "nist_role_id": "NIST 工作角色 ID",
        "salary_roadmap_2026": "2026 薪資與認證路線圖",
        "salary_range": "典型薪資區間（2026）：",
        "cert_roadmap": "認證路徑：",
        "phase_instinct": "直覺（性格）",
        "phase_technical": "技術（分流）",
        "phase_deep": "深度情境（2026+ 趨勢）",
        "status_idle": "閒置",
        "status_phase1": "第一階段 — 直覺",
        "status_phase2": "第二階段 — 技術",
        "status_phase3": "第三階段 — 深度情境",
        "phase_tks": "TKS 缺口（2026 NIST）",
        "status_phase4": "第四階段 — TKS",
        "status_complete": "完成",
        "question_label": "請選擇一項：",
        "submit_btn": "送出",
        "results_title": "評估完成",
        "work_role": "工作角色",
        "your_strengths": "您的優勢",
        "category_fit": "NICE 類別契合（7 類別）",
        "role_probability": "角色機率",
        "recommended_roadmap": "推薦路線圖",
        "download_pdf": "下載為 PDF",
        "align_success": "依 NICE 架構規劃您的職涯。",
        "start_over": "重新開始",
        "sidebar_title": "代理狀態",
        "sidebar_status": "狀態",
        "sidebar_question": "題目",
        "sidebar_progress": "進度",
        "sidebar_footer": "NIST NICE Framework · Cyber Career Compass",
        "answered": "已答",
        "of": "／",
        "please_choose": "請先選擇一項再送出。",
        "skill_heatmap_title": "技能熱力圖",
        "install_fpdf2": "下載 PDF 請安裝 fpdf2：pip install fpdf2",
        "pdf_title": "NICE 職涯 Dossier",
        "pdf_work_role": "工作角色",
        "pdf_category": "類別",
        "pdf_strengths": "您的優勢",
        "pdf_category_profile": "類別概況（0–100 正規化）",
        "pdf_certs": "推薦認證",
        "language_label": "語言",
        "archetype_builder": "建構者",
        "archetype_builder_desc": "您設計與建置安全系統。擅長架構、安全開發與韌性基礎設施。",
        "archetype_guardian": "守護者",
        "archetype_guardian_desc": "您保護與防禦。在 SOC、事件應變與即時威脅圍堵中表現出色。",
        "archetype_investigator": "調查者",
        "archetype_investigator_desc": "您分析與調查。串聯資料、產出情資並建立案情。",
        "archetype_operator": "維運者",
        "archetype_operator_desc": "您營運與維護。透過維運、監控與持續合規守護系統。",
        "archetype_governor": "治理者",
        "archetype_governor_desc": "您監督與治理。將資安與策略、風險及法規要求對齊。",
        "reflex_system_health_label": "系統狀態",
        "reflex_system_nominal": "系統正常",
        "reflex_complete_btn": "完成試煉",
        "reflex_neutralize": "中和",
        "reflex_drop": "丟棄",
        "reflex_freeze": "凍結",
        "reflex_incorrect_try": "不正確。",
        "pg_scores_synced": "分數已同步至 C3S 雷達。您的 NICE 對齊已更新。",
    }


# ─── Question texts: prompt + list of choice strings (weights come from questions.py) ───
# Instinct: 5 questions, 3 choices each
# Technical: 10 questions, 4 choices each
# Deep: 20 questions, 3 choices each; 20th is regional (METI for JA, regional for EN/ZH)

def _instinct_en() -> List[Dict[str, Any]]:
    return [
        {"prompt": "When something breaks in production, your first instinct is to:", "choices": [
            "Design a fix and improve the system so it doesn't happen again.",
            "Contain the impact and protect users while others fix it.",
            "Trace the root cause and document what happened before changing anything.",
        ]},
        {"prompt": "You're most energized when:", "choices": [
            "Creating or improving a secure product or architecture.",
            "Stopping an attack or defending a critical asset.",
            "Uncovering how an attacker got in or what they were after.",
        ]},
        {"prompt": "In a team crisis, you naturally:", "choices": [
            "Propose a new process or tool to prevent recurrence.",
            "Take charge of communication and containment.",
            "Gather evidence and timeline before assigning blame.",
        ]},
        {"prompt": "Your ideal project is one where you:", "choices": [
            "Build something that stays secure by design.",
            "Monitor and respond to real-world threats.",
            "Analyze patterns and produce intelligence others act on.",
        ]},
        {"prompt": "Feedback you value most is:", "choices": [
            "'The system you designed held up under stress.'",
            "'Your response saved us from a major breach.'",
            "'Your analysis changed how we see the threat landscape.'",
        ]},
    ]


def _instinct_ja() -> List[Dict[str, Any]]:
    return [
        {"prompt": "本番で障害が起きたとき、まず何をしますか？", "choices": [
            "修正を設計し、再発しないようシステムを改善する。",
            "影響を封じ込め、他が修正する間ユーザーを守る。",
            "変更前に根本原因を追い、経緯を記録する。",
        ]},
        {"prompt": "最もエネルギーが湧くのは：", "choices": [
            "セキュアな製品やアーキテクチャを作り・改善するとき。",
            "攻撃を止めたり重要資産を守ったりするとき。",
            "攻撃者の侵入経路や目的を解明するとき。",
        ]},
        {"prompt": "チームの危機では、自然と：", "choices": [
            "再発防止のためのプロセスやツールを提案する。",
            "連絡と封じ込めの指揮を取る。",
            "証拠とタイムラインを集めてから責任を問う。",
        ]},
        {"prompt": "理想のプロジェクトは：", "choices": [
            "設計でセキュアなものを構築するプロジェクト。",
            "実世界の脅威を監視・対応するプロジェクト。",
            "パターンを分析し他が使うインテリジェンスを出すプロジェクト。",
        ]},
        {"prompt": "最も嬉しいフィードバックは：", "choices": [
            "「設計したシステムがストレス下で持った」。",
            "「あなたの対応で重大侵害を防げた」。",
            "「分析で脅威の見え方が変わった」。",
        ]},
    ]


def _instinct_zh_tw() -> List[Dict[str, Any]]:
    return [
        {"prompt": "當生產環境出問題時，您的第一反應是：", "choices": [
            "設計修復並改善系統，避免再發生。",
            "控制影響、保護使用者，由他人修復。",
            "先追根究底並記錄經過，再進行變更。",
        ]},
        {"prompt": "您最有動力的情境是：", "choices": [
            "建立或改進安全產品或架構。",
            "阻止攻擊或守護關鍵資產。",
            "找出攻擊者如何入侵或目的為何。",
        ]},
        {"prompt": "在團隊危機中，您通常：", "choices": [
            "提出新流程或工具以防再發生。",
            "負責溝通與圍堵。",
            "先蒐集證據與時間軸再究責。",
        ]},
        {"prompt": "您理想的專案是：", "choices": [
            "從設計就保持安全的建置。",
            "監控並因應真實威脅。",
            "分析模式並產出他人可用的情資。",
        ]},
        {"prompt": "您最在意的回饋是：", "choices": [
            "「你設計的系統在壓力下撐住了。」",
            "「你的應變讓我們免於重大侵害。」",
            "「你的分析改變了我們對威脅的認知。」",
        ]},
    ]


# Technical: 10 questions, 4 choices (canonical EN only here; JA/ZH can be added similarly)
def _technical_en() -> List[Dict[str, Any]]:
    return [
        {"prompt": "What does 'defense in depth' emphasize?", "choices": [
            "Multiple layers of security controls so one failure doesn't compromise the system.",
            "A single strong firewall at the perimeter.",
            "Encryption only.",
            "Physical security only.",
        ]},
        {"prompt": "Which best describes a zero-trust approach?", "choices": [
            "Never trust, always verify; assume breach.",
            "Trust only the internal network.",
            "Trust only after one login.",
            "Trust only physical access.",
        ]},
        {"prompt": "What is the primary goal of an incident response plan?", "choices": [
            "Contain, eradicate, recover, and learn from security incidents.",
            "Prevent all incidents from ever occurring.",
            "Blame the right team.",
            "Only document incidents.",
        ]},
        {"prompt": "What does 'phishing' typically rely on?", "choices": [
            "Social engineering and deceptive communication to steal credentials or data.",
            "Only technical exploits in software.",
            "Physical theft of devices.",
            "Encryption weaknesses.",
        ]},
        {"prompt": "Why is patch management important?", "choices": [
            "To fix known vulnerabilities and reduce attack surface.",
            "Only to add new features.",
            "To slow down systems.",
            "Only for compliance paperwork.",
        ]},
        {"prompt": "What is the role of multi-factor authentication (MFA)?", "choices": [
            "Require more than one proof of identity to reduce risk of credential compromise.",
            "Replace passwords entirely with one factor.",
            "Only for high-level executives.",
            "To simplify login.",
        ]},
        {"prompt": "What does 'least privilege' mean?", "choices": [
            "Users and processes get only the minimum access needed to do their job.",
            "Everyone gets admin rights for convenience.",
            "Only one person has any access.",
            "Privilege is based on job title only.",
        ]},
        {"prompt": "Why is logging and monitoring important in security?", "choices": [
            "To detect anomalies, investigate incidents, and support accountability.",
            "Only for compliance audits.",
            "To slow down systems.",
            "To replace firewalls.",
        ]},
        {"prompt": "What is a common goal of security awareness training?", "choices": [
            "Reduce human error and improve recognition of social engineering.",
            "Replace all technical controls.",
            "Only to satisfy auditors.",
            "To teach everyone to code.",
        ]},
        {"prompt": "What does 'confidentiality, integrity, availability' (CIA triad) represent?", "choices": [
            "Core security objectives: protect secrecy, accuracy, and access to data/systems.",
            "A single tool that does everything.",
            "Only physical security.",
            "A government agency.",
        ]},
    ]


# Deep scenario: 16 total. 15 common (5 trend + 10 NIST); 16th is regional (METI for JA, regional for EN/ZH).
def _deep_common_en() -> List[Dict[str, Any]]:
    """15 deep scenario questions: 5 trend (AI/Quantum) + 10 NIST NICE task–based."""
    return [
        # —— 5 trend (reduced from 10) ——
        {"prompt": "Your organization is rolling out an AI-powered threat detection tool. Your priority is to:", "choices": [
            "Define secure development and validation criteria so the model isn't poisoned or evaded.",
            "Monitor live alerts and tune response playbooks when the AI flags incidents.",
            "Audit the training data and model behavior to document risks and explainability.",
        ]},
        {"prompt": "A critical vendor in your supply chain reports a breach. Your first focus is:", "choices": [
            "Harden procurement and vendor assessment so future contracts enforce security requirements.",
            "Contain exposure: isolate affected systems and coordinate with the vendor on containment.",
            "Map the vendor's access and data flows, then produce a risk assessment for leadership.",
        ]},
        {"prompt": "Cloud governance is being centralized. You prefer to:", "choices": [
            "Design and implement guardrails (e.g., IaC policies, landing zones) so teams can move fast safely.",
            "Operate and maintain the secure baseline: patch, monitor, and respond to misconfigurations.",
            "Analyze cloud activity and compliance drift to report gaps and recommend controls.",
        ]},
        {"prompt": "You discover a third-party library used in your app has a critical CVE. Your instinct is to:", "choices": [
            "Patch or replace the dependency and add SBOM and dependency checks to the pipeline.",
            "Assess impact, apply mitigations, and coordinate with ops and dev for a fix.",
            "Trace where the library is used and document the blast radius for incident and risk reports.",
        ]},
        {"prompt": "Leadership asks how to prepare for AI-driven attacks (e.g., deepfakes, automated exploits). You emphasize:", "choices": [
            "Building security into AI systems and defenses (e.g., adversarial testing, model assurance).",
            "Strengthening detection and response so we can recognize and contain novel attack patterns.",
            "Investing in threat intelligence and forensics to understand and attribute AI-enabled campaigns.",
        ]},
        # —— 10 NIST NICE task–based questions ——
        {"prompt": "Your organization is implementing the Risk Management Framework (RMF). Your primary task is to:", "choices": [
            "Categorize the system, select and tailor NIST SP 800-53 controls, and document the security plan.",
            "Execute continuous monitoring and report control status to the authorizing official.",
            "Conduct security assessments and produce the authorization package for the AO.",
        ]},
        {"prompt": "During incident triage, you prioritize events by:", "choices": [
            "Impact to confidentiality, integrity, availability and alignment with the incident response plan.",
            "Order of arrival so no ticket is left behind.",
            "Which system generated the alert, regardless of business criticality.",
        ]},
        {"prompt": "A security control assessment (SCA) is due. You focus on:", "choices": [
            "Testing controls per NIST SP 800-53A and documenting findings with evidence and remediation plans.",
            "Running the scanning tools and forwarding reports to the assessment team.",
            "Drafting the system security plan and leaving testing to the assessor.",
        ]},
        {"prompt": "Contingency planning for a critical system requires:", "choices": [
            "Documented contingency plans, tested backup/restore, and alignment with recovery objectives (RTO/RPO).",
            "Only maintaining backups; restoration is handled during an incident.",
            "A single annual tabletop exercise with no updates to the plan.",
        ]},
        {"prompt": "Vulnerability management (scanning and remediation) is most effective when:", "choices": [
            "Scans are scheduled, results are risk-ranked and assigned to owners, and remediation is tracked to closure.",
            "Scans run only after a major incident.",
            "All findings are treated equally and patching is done only during maintenance windows.",
        ]},
        {"prompt": "To achieve Authority to Operate (ATO), you ensure:", "choices": [
            "The security assessment is complete, the authorization package is ready, and the AO can make a risk-based decision.",
            "All controls are fully implemented with no exceptions before the assessment.",
            "Only the system owner signs the authorization; no AO is required.",
        ]},
        {"prompt": "Security awareness training is designed to support NICE tasks when:", "choices": [
            "Content is role-based, covers policy and threats (e.g., phishing), and is measured by behavior and knowledge checks.",
            "Everyone watches the same annual video with no assessment.",
            "Training is optional and only for new hires.",
        ]},
        {"prompt": "As incident response coordinator, your first steps after declaration are:", "choices": [
            "Activate the IR plan, assign roles, establish communication channels, and begin containment and evidence preservation.",
            "Wait for management to decide whether to respond.",
            "Start forensic imaging on all systems before containing the threat.",
        ]},
        {"prompt": "A security architecture review of a new application should address:", "choices": [
            "Data flows, trust boundaries, authentication/authorization, and alignment with security requirements and standards.",
            "Only whether the vendor is reputable.",
            "Only the look and feel of the login page.",
        ]},
        {"prompt": "Security operations use cases (e.g., in a SIEM) should be:", "choices": [
            "Tied to threats and controls, tuned to reduce false positives, and reviewed for coverage and effectiveness.",
            "Left at default and never updated.",
            "Defined only after a major breach.",
        ]},
    ]


# Specialist path: 19 TKS (Task, Knowledge, Skill) gap questions for 50-question full analysis.
def _specialist_tks_en() -> List[Dict[str, Any]]:
    return [
        {"prompt": "When evaluating a vendor's security posture (TKS), you prioritize:", "choices": [
            "Documented controls, attestations, and continuous monitoring evidence.",
            "A single questionnaire completed annually.",
            "Trust based on brand name only.",
        ]},
        {"prompt": "NIST SP 800-53 Rev. 5 control selection should be:", "choices": [
            "Risk-based: tailor controls to the system and threat environment.",
            "Implement every control regardless of relevance.",
            "Deferred until after deployment.",
        ]},
        {"prompt": "Security testing in CI/CD (TKS) is most effective when:", "choices": [
            "SAST, DAST, and dependency checks run on every pipeline run with defined gates.",
            "Only manual testing before release.",
            "Testing is skipped to meet deadlines.",
        ]},
        {"prompt": "For supply chain risk (e.g., OG-WRL-017), you focus on:", "choices": [
            "Supplier assessments, SBOMs, and contract security requirements.",
            "Only using well-known vendors.",
            "No formal process.",
        ]},
        {"prompt": "DevSecOps (NF-COM-008) culture requires:", "choices": [
            "Shared ownership of security across dev, sec, and ops with automation.",
            "Security team gate at the end of the pipeline only.",
            "Separate security team with no dev involvement.",
        ]},
        {"prompt": "Incident triage (TKS) should prioritize by:", "choices": [
            "Impact to CIA and business criticality; then by containment urgency.",
            "First-in-first-out only.",
            "Only by severity label.",
        ]},
        {"prompt": "Zero Trust architecture (2026 focus) emphasizes:", "choices": [
            "Verify explicitly, least privilege, assume breach; identity and context everywhere.",
            "Strong perimeter only.",
            "VPN and firewall only.",
        ]},
        {"prompt": "Cloud security posture management (CSPM) is used to:", "choices": [
            "Continuously detect and remediate misconfigurations and compliance drift.",
            "Run one-time audits only.",
            "Replace identity management.",
        ]},
        {"prompt": "Threat intelligence (TKS) should be:", "choices": [
            "Actionable, integrated into detection and response; updated regularly.",
            "Collected but not used operationally.",
            "Only from a single source.",
        ]},
        {"prompt": "Security awareness (TKS) effectiveness is measured by:", "choices": [
            "Behavior change, phishing simulation results, and knowledge assessments.",
            "Attendance only.",
            "Not measured.",
        ]},
        {"prompt": "Ransomware response (2026) should include:", "choices": [
            "Containment, isolation, evidence preservation, and recovery from known-good backups.",
            "Immediate payment to restore access.",
            "Only rebuilding from scratch.",
        ]},
        {"prompt": "API security (TKS) requires:", "choices": [
            "Authentication, authorization, rate limiting, and input validation.",
            "Only HTTPS.",
            "No special measures.",
        ]},
        {"prompt": "Privacy by design (TKS) means:", "choices": [
            "Embed privacy and data minimization into system design and lifecycle.",
            "Adding a privacy policy at the end.",
            "Only compliance paperwork.",
        ]},
        {"prompt": "Security orchestration (SOAR) is best used for:", "choices": [
            "Automating playbooks, enrichment, and response actions to scale SOC.",
            "Replacing analysts entirely.",
            "Only for reporting.",
        ]},
        {"prompt": "Red team exercises (TKS) should:", "choices": [
            "Simulate real adversaries and test detection and response end-to-end.",
            "Only test technical controls in isolation.",
            "Be avoided to prevent disruption.",
        ]},
        {"prompt": "Third-party risk (OG-WRL-017) lifecycle includes:", "choices": [
            "Due diligence, contract requirements, continuous monitoring, and offboarding.",
            "One-time assessment only.",
            "No formal lifecycle.",
        ]},
        {"prompt": "Secure coding (TKS) standards should be:", "choices": [
            "Integrated into IDE and pipeline; enforced with training and reviews.",
            "Optional guidelines only.",
            "Not adopted.",
        ]},
        {"prompt": "Board-level security reporting (TKS) should emphasize:", "choices": [
            "Risk posture, key metrics, and alignment with business and regulatory goals.",
            "Technical jargon only.",
            "Only when an incident occurs.",
        ]},
        {"prompt": "Identity governance (2026) includes:", "choices": [
            "Lifecycle management, access reviews, and least privilege enforcement.",
            "Only provisioning accounts.",
            "No governance process.",
        ]},
    ]


def get_specialist_tks_texts(lang: str) -> List[Dict[str, Any]]:
    return _specialist_tks_en()


# Operator path: 12 branching 2026 mission scenarios (AI + Supply Chain).
def _operator_mission_en() -> List[Dict[str, Any]]:
    return [
        {"prompt": "[Mission 1 — AI] Your organization is deploying an LLM for customer support. A red team finds prompt injection risks. You:", "choices": [
            "Implement input/output validation, rate limits, and adversarial testing in the pipeline.",
            "Delay launch until the vendor patches the model.",
            "Accept the risk and document it for leadership.",
        ]},
        {"prompt": "[Mission 2 — Supply Chain] A critical software vendor is acquired. You must reassess risk. You:", "choices": [
            "Re-run due diligence, review new ownership controls, and update contracts and monitoring.",
            "Assume the new owner maintains the same security posture.",
            "Terminate the contract immediately.",
        ]},
        {"prompt": "[Mission 3 — AI] AI-generated deepfakes are used in a business email compromise attempt. You:", "choices": [
            "Enhance identity verification, awareness training, and technical controls for media authenticity.",
            "Block all external media in email.",
            "Rely only on user vigilance.",
        ]},
        {"prompt": "[Mission 4 — Supply Chain] A component in your SBOM has a critical CVE. You:", "choices": [
            "Assess blast radius, apply mitigations or patches, and track remediation; update SBOM.",
            "Wait for the next release cycle to patch.",
            "Remove the component without replacement.",
        ]},
        {"prompt": "[Mission 5 — AI] An AI-based SOC tool produces too many false positives. You:", "choices": [
            "Tune detection rules, enrich with context, and define escalation criteria with the team.",
            "Disable the tool.",
            "Ignore low-severity alerts.",
        ]},
        {"prompt": "[Mission 6 — Supply Chain] You must onboard a new supplier (OG-WRL-017). You prioritize:", "choices": [
            "Security questionnaire, control evidence, and contract clauses for ongoing assessment.",
            "Only a signed NDA.",
            "No formal process.",
        ]},
        {"prompt": "[Mission 7 — AI] Leadership wants to use generative AI for internal documents. You:", "choices": [
            "Define data boundaries, access controls, and acceptable use; then pilot with guardrails.",
            "Block all use of generative AI.",
            "Allow unrestricted use.",
        ]},
        {"prompt": "[Mission 8 — Supply Chain] A key logistics partner suffers a breach. You:", "choices": [
            "Activate supply chain incident playbook: contain exposure, assess impact, communicate with stakeholders.",
            "Wait for the partner to notify you.",
            "Switch partners immediately.",
        ]},
        {"prompt": "[Mission 9 — AI] Model drift is affecting your AI threat detection. You:", "choices": [
            "Establish monitoring, retraining triggers, and validation against current threats.",
            "Retrain only when accuracy drops below a threshold.",
            "Discontinue the model.",
        ]},
        {"prompt": "[Mission 10 — Supply Chain] You need to justify supply chain security investment to the board. You:", "choices": [
            "Present risk scenarios, regulatory drivers, and ROI of reduced incident impact.",
            "Request budget without metrics.",
            "Skip the request.",
        ]},
        {"prompt": "[Mission 11 — AI] An AI system is making biased decisions. You:", "choices": [
            "Audit training data and model outputs; implement fairness checks and human oversight.",
            "Disable the system without investigation.",
            "Leave the system as is.",
        ]},
        {"prompt": "[Mission 12 — Supply Chain] NIST CSF 2.0 emphasizes supply chain. You:", "choices": [
            "Map supply chain risks to the GOVERN pillar and integrate into risk management.",
            "Treat supply chain as a separate program.",
            "Defer until required by regulation.",
        ]},
    ]


# Branching narrative: Mission 2 and 3 variants by prior choice (0=technical, 1=policy, 2=hybrid/accept)
OPERATOR_BRANCH_VARIANTS_EN: Dict[int, List[Dict[str, Any]]] = {
    1: [
        {"prompt": "[Mission 2 — Technical Escalation] The pipeline fix triggers a design review. Security architecture asks for threat model updates. You:", "choices": [
            "Update the threat model, document assumptions, and add abuse cases for the LLM interface.",
            "Defer the review until after launch.",
            "Hand off to the vendor.",
        ]},
        {"prompt": "[Mission 2 — Board Briefing] Leadership requests a risk briefing before launch. You:", "choices": [
            "Present residual risk, mitigations, and a go/no-go recommendation with clear criteria.",
            "Recommend delay without metrics.",
            "Approve launch without formal briefing.",
        ]},
        {"prompt": "[Mission 2 — Follow-up] Governance asks for documented mitigations after you accepted the risk. You:", "choices": [
            "Document compensating controls, monitoring, and a review timeline.",
            "Push back that risk was already accepted.",
            "Skip documentation.",
        ]},
    ],
    2: [
        {"prompt": "[Mission 3 — Technical Path] The vendor reassessment reveals new integration points. You:", "choices": [
            "Map new data flows and trigger a focused assessment on the integration layer.",
            "Assume the acquisition does not change integration risk.",
            "Pause all integrations until full audit.",
        ]},
        {"prompt": "[Mission 3 — Policy Path] The board wants supply chain risk in the next quarter report. You:", "choices": [
            "Draft a supply chain risk section with key metrics and top vendor status.",
            "Include a one-line summary only.",
            "Omit supply chain from the report.",
        ]},
        {"prompt": "[Mission 3 — Hybrid] You need to align technical and governance views on the acquired vendor. You:", "choices": [
            "Convene a short cross-functional session and document agreed controls and ownership.",
            "Let technical and governance work in silos.",
            "Escalate to leadership without options.",
        ]},
    ],
}


# Line 907: parameter must be Optional[int]) — not Optional[int]] (extra ] causes SyntaxError)
def get_operator_texts_branch(lang: str, index: int, prior_choice: Optional[int]) -> Optional[Dict[str, Any]]:
    """Return Operator mission prompt+choices for index; if index is 1 or 2, use branch variant from prior_choice."""
    base = _operator_mission_en()
    if index < 0 or index >= len(base):
        return None
    if index in (1, 2) and prior_choice is not None and 0 <= prior_choice <= 2:
        variants = OPERATOR_BRANCH_VARIANTS_EN.get(index, [])
        if prior_choice < len(variants):
            return variants[prior_choice]
    return base[index]


def get_operator_texts(lang: str) -> List[Dict[str, Any]]:
    return _operator_mission_en()


# 20th question: regional. METI for Japan; generic regional for EN/ZH.
DEEP_REGIONAL_EN: Dict[str, Any] = {
    "prompt": "Your organization must align with a regional cybersecurity framework (e.g., NIST CSF, sector guidelines). You prioritize:",
    "choices": [
        "Mapping existing controls to the framework and closing gaps with a prioritized roadmap.",
        "Ensuring operations and monitoring support continuous compliance and evidence collection.",
        "Producing executive summaries and audit-ready reports for regulators and boards.",
    ],
}

DEEP_REGIONAL_JA: Dict[str, Any] = {
    "prompt": "経済産業省（METI）の「サイバーセキュリティ経営ガイドライン」に沿って経営層に説明する場合、あなたは何を重視しますか？",
    "choices": [
        "ガイドラインの「重要10項目」を自社の対策にマッピングし、ギャップとロードマップを提示する。",
        "インシデント対応とBCP、サプライチェーン管理の実態を説明し、経営の責務を明確にする。",
        "監査・規制対応用の証拠と報告書を整備し、説明責任を果たす。",
    ],
}

DEEP_REGIONAL_ZH_TW: Dict[str, Any] = {
    "prompt": "組織需符合區域資安法規（如個資法、資通安全法）時，您會優先：",
    "choices": [
        "將現有控制措施對應法規要求，並以優先序排定改善路線圖。",
        "確保維運與監控能持續符合要求並留存證據。",
        "產出可供主管機關與董事會查閱的摘要與報告。",
    ],
}


def get_instinct_texts(lang: str) -> List[Dict[str, Any]]:
    if lang == "ja":
        return _instinct_ja()
    if lang == "zh_tw":
        return _instinct_zh_tw()
    return _instinct_en()


# Explorer path: 5 extra instinct questions (10 total = 5 instinct + 5 here)
def _explorer_extra_instinct_en() -> List[Dict[str, Any]]:
    return [
        {"prompt": "When you learn a new security tool, you prefer to:", "choices": [
            "Design how it fits into the broader architecture and document patterns.",
            "Run it in a lab and practice response playbooks.",
            "Dig into the data it produces and look for anomalies.",
        ]},
        {"prompt": "Your ideal team role is:", "choices": [
            "Designing and implementing controls so the rest of the team can operate safely.",
            "Being on the front line when something breaks or an alert fires.",
            "Researching threats and producing reports that others act on.",
        ]},
        {"prompt": "When a new policy is released, you:", "choices": [
            "Map it to existing controls and plan implementation.",
            "Focus on how to monitor and enforce it in operations.",
            "Analyze gaps and recommend changes for leadership.",
        ]},
        {"prompt": "You're most satisfied when:", "choices": [
            "A system you built passes a security review.",
            "You contained an incident before it spread.",
            "Your analysis led to a decision that reduced risk.",
        ]},
        {"prompt": "In a cross-functional project, you naturally:", "choices": [
            "Own the security design and integration points.",
            "Own the runbooks and escalation paths.",
            "Own the risk assessment and reporting.",
        ]},
    ]


def _explorer_extra_instinct_ja() -> List[Dict[str, Any]]:
    return [
        {"prompt": "新しいセキュリティツールを学ぶとき、あなたは：", "choices": [
            "全体アーキテクチャへの組み立て方とパターンを文書化する。",
            "ラボで動かし、対応プレイブックを練習する。",
            "ツールが出力するデータを掘り、異常を探す。",
        ]},
        {"prompt": "理想のチーム役割は：", "choices": [
            "コントロールを設計・実装し、他メンバーが安全に運用できるようにする。",
            "障害やアラートの最前線に立つ。",
            "脅威を調査し、他が行動するレポートを出す。",
        ]},
        {"prompt": "新ポリシーが発表されると、あなたは：", "choices": [
            "既存コントロールにマッピングし、実装を計画する。",
            "運用でどう監視・執行するかに集中する。",
            "ギャップを分析し、経営向けに変更を提案する。",
        ]},
        {"prompt": "最も満足するのは：", "choices": [
            "自分が作ったシステムがセキュリティレビューを通過したとき。",
            "インシデントが広がる前に封じ込めたとき。",
            "自分の分析がリスク低減の意思決定につながったとき。",
        ]},
        {"prompt": "横断プロジェクトでは、自然と：", "choices": [
            "セキュリティ設計と連携ポイントを担当する。",
            "ランブックとエスカレーションを担当する。",
            "リスク評価と報告を担当する。",
        ]},
    ]


def _explorer_extra_instinct_zh_tw() -> List[Dict[str, Any]]:
    return [
        {"prompt": "學習新資安工具時，您偏好：", "choices": [
            "設計它如何融入整體架構並撰寫模式文件。",
            "在實驗環境演練並練習應變劇本。",
            "深入其產出的資料並尋找異常。",
        ]},
        {"prompt": "您理想的團隊角色是：", "choices": [
            "設計與實作控制措施，讓團隊能安全營運。",
            "在出事或告警時站在第一線。",
            "研究威脅並產出供他人行動的報告。",
        ]},
        {"prompt": "新政策發布時，您會：", "choices": [
            "對應既有控制並規劃實作。",
            "專注於如何在維運中監控與執行。",
            "分析落差並向主管建議調整。",
        ]},
        {"prompt": "您最有成就感的是：", "choices": [
            "您建置的系統通過安全審查。",
            "在事件擴散前完成圍堵。",
            "您的分析促成降低風險的決策。",
        ]},
        {"prompt": "在跨職能專案中，您自然會：", "choices": [
            "負責資安設計與介面整合。",
            "負責維運手冊與升級路徑。",
            "負責風險評估與報告。",
        ]},
    ]


def get_explorer_instinct_texts(lang: str) -> List[Dict[str, Any]]:
    """10 questions for Explorer path: 5 instinct + 5 extra."""
    base = get_instinct_texts(lang)
    if lang == "ja":
        extra = _explorer_extra_instinct_ja()
    elif lang == "zh_tw":
        extra = _explorer_extra_instinct_zh_tw()
    else:
        extra = _explorer_extra_instinct_en()
    return base + extra


def get_technical_texts(lang: str) -> List[Dict[str, Any]]:
    # JA/ZH technical can be added; for now use EN for all
    return _technical_en()


def get_deep_texts(lang: str) -> List[Dict[str, Any]]:
    common = _deep_common_en()
    if lang == "ja":
        regional = DEEP_REGIONAL_JA
    elif lang == "zh_tw":
        regional = DEEP_REGIONAL_ZH_TW
    else:
        regional = DEEP_REGIONAL_EN
    return common + [regional]


def get_role_labels(lang: str) -> Dict[str, str]:
    """Work role short names for Role Probability radar (including 2026 NIST)."""
    base = {
        "SP-SSE": "SP-SSE",
        "SP-ARC": "SP-ARC",
        "PR-CDA": "PR-CDA",
        "PR-IR": "PR-IR",
        "AN-TWA": "AN-TWA",
        "IN-CLI": "IN-CLI",
        "OG-WRL-017": "OG-WRL-017",
        "NF-COM-008": "NF-COM-008",
    }
    return dict(base)


# ─── NIST Work Role display strings (title, definition, strengths, category) per language ───
def _roles_en() -> Dict[str, Dict[str, str]]:
    return {
        "SP-SSE": {
            "title": "Secure Software Assessor",
            "category": "Securely Provision (SP)",
            "definition": "Assesses the security of software and systems through testing and analysis.",
            "strengths": "You excel at structured assessment and building security into the development lifecycle.",
        },
        "SP-ARC": {
            "title": "Security Architect",
            "category": "Securely Provision (SP)",
            "definition": "Designs and builds secure systems, networks, and architectures.",
            "strengths": "You combine design thinking with security principles to create resilient systems.",
        },
        "PR-CDA": {
            "title": "Cyber Defense Analyst",
            "category": "Protect and Defend (PR)",
            "definition": "Monitors and analyzes events to protect systems and respond to incidents.",
            "strengths": "You thrive in defending systems and responding to threats in real time.",
        },
        "PR-IR": {
            "title": "Incident Responder",
            "category": "Protect and Defend (PR)",
            "definition": "Investigates and mitigates security incidents and coordinates response activities.",
            "strengths": "You lead under pressure and coordinate teams to contain and remediate incidents.",
        },
        "AN-TWA": {
            "title": "Threat/Warning Analyst",
            "category": "Analyze (AN)",
            "definition": "Analyzes threat data and produces assessments and warnings for decision makers.",
            "strengths": "You connect dots across data to surface threats and inform strategy.",
        },
        "IN-CLI": {
            "title": "Cyber Crime Investigator",
            "category": "Investigate (IN)",
            "definition": "Investigates cyber crimes and compiles evidence for legal proceedings.",
            "strengths": "You pursue leads methodically and build cases that stand up to scrutiny.",
        },
        "OG-WRL-017": {
            "title": "Supply Chain Risk Manager",
            "category": "Oversee and Govern (OV)",
            "definition": "Manages cybersecurity risk across the supply chain; aligns with 2026 NIST NICE updates for third-party and vendor risk.",
            "strengths": "You excel at assessing vendor security, contract requirements, and end-to-end supply chain resilience.",
        },
        "NF-COM-008": {
            "title": "DevSecOps Engineer",
            "category": "Securely Provision (SP)",
            "definition": "Integrates security into development and operations; maps to 2026 NIST NICE DevSecOps and continuous delivery.",
            "strengths": "You bridge development, security, and operations with automation and secure pipelines.",
        },
    }


def _roles_ja() -> Dict[str, Dict[str, str]]:
    return {
        "SP-SSE": {
            "title": "セキュアソフトウェアアセスター",
            "category": "安全に提供 (SP)",
            "definition": "テストと分析によりソフトウェアおよびシステムのセキュリティを評価します。",
            "strengths": "構造化された評価と開発ライフサイクルへのセキュリティ組み込みが得意です。",
        },
        "SP-ARC": {
            "title": "セキュリティアーキテクト",
            "category": "安全に提供 (SP)",
            "definition": "セキュアなシステム・ネットワーク・アーキテクチャを設計・構築します。",
            "strengths": "デザイン思考とセキュリティ原則を組み合わせ、耐障害性の高いシステムを作ります。",
        },
        "PR-CDA": {
            "title": "サイバー防御アナリスト",
            "category": "保護・防御 (PR)",
            "definition": "システムを保護しインシデントに対応するため、イベントを監視・分析します。",
            "strengths": "システムの防御とリアルタイムの脅威対応で力を発揮します。",
        },
        "PR-IR": {
            "title": "インシデントレスポンダー",
            "category": "保護・防御 (PR)",
            "definition": "セキュリティインシデントの調査・軽減と対応活動の調整を行います。",
            "strengths": "プレッシャー下で指揮し、封じ込めと復旧のためにチームをまとめます。",
        },
        "AN-TWA": {
            "title": "脅威・警告アナリスト",
            "category": "分析 (AN)",
            "definition": "脅威データを分析し、意思決定者向けの評価と警告を提供します。",
            "strengths": "データをつなぎ合わせて脅威を可視化し、戦略に貢献します。",
        },
        "IN-CLI": {
            "title": "サイバー犯罪捜査官",
            "category": "調査 (IN)",
            "definition": "サイバー犯罪を調査し、法的手続きのための証拠をまとめます。",
            "strengths": "リードを体系的に追い、精査に耐えるケースを構築します。",
        },
        "OG-WRL-017": {
            "title": "サプライチェーンリスクマネージャー",
            "category": "監督・統治 (OV)",
            "definition": "サプライチェーン全体のサイバーセキュリティリスクを管理。2026 NIST NICE に準拠した第三者・ベンダーリスク。",
            "strengths": "ベンダーセキュリティ評価、契約要件、エンドツーエンドのレジリエンスに強み。",
        },
        "NF-COM-008": {
            "title": "DevSecOps エンジニア",
            "category": "安全に提供 (SP)",
            "definition": "開発と運用にセキュリティを統合。2026 NIST NICE DevSecOps・継続的デリバリーにマッピング。",
            "strengths": "開発・セキュリティ・運用を自動化とセキュアパイプラインでつなぎます。",
        },
    }


def _roles_zh_tw() -> Dict[str, Dict[str, str]]:
    return {
        "SP-SSE": {
            "title": "安全軟體評估員",
            "category": "安全維運 (SP)",
            "definition": "透過測試與分析評估軟體與系統的安全性。",
            "strengths": "您擅長結構化評估並將安全納入開發生命週期。",
        },
        "SP-ARC": {
            "title": "安全架構師",
            "category": "安全維運 (SP)",
            "definition": "設計與建置安全系統、網路與架構。",
            "strengths": "您結合設計思維與安全原則，建立具韌性的系統。",
        },
        "PR-CDA": {
            "title": "資安防禦分析師",
            "category": "保護與防禦 (PR)",
            "definition": "監控與分析事件以保護系統並因應事件。",
            "strengths": "您擅長防禦系統並即時因應威脅。",
        },
        "PR-IR": {
            "title": "事件應變人員",
            "category": "保護與防禦 (PR)",
            "definition": "調查與減緩安全事件並協調應變活動。",
            "strengths": "您能在壓力下領導並協調團隊進行圍堵與修復。",
        },
        "AN-TWA": {
            "title": "威脅／預警分析師",
            "category": "分析 (AN)",
            "definition": "分析威脅資料並產出供決策者使用的評估與預警。",
            "strengths": "您能串聯資料以發現威脅並支援策略。",
        },
        "IN-CLI": {
            "title": "網路犯罪調查員",
            "category": "調查 (IN)",
            "definition": "調查網路犯罪並彙整法律程序所需證據。",
            "strengths": "您有條理地追查線索並建立經得起檢驗的案情。",
        },
        "OG-WRL-017": {
            "title": "供應鏈風險管理",
            "category": "監督與治理 (OV)",
            "definition": "管理供應鏈中的資安風險；對應 2026 NIST NICE 第三方與供應商風險。",
            "strengths": "您擅長評估供應商安全、合約要求與端到端供應鏈韌性。",
        },
        "NF-COM-008": {
            "title": "DevSecOps 工程師",
            "category": "安全維運 (SP)",
            "definition": "將安全整合至開發與維運；對應 2026 NIST NICE DevSecOps 與持續交付。",
            "strengths": "您以自動化與安全管道串聯開發、資安與維運。",
        },
    }


def _learning_objectives_en() -> Dict[str, List[str]]:
    """Learning objectives per NICE category (EN). Used in Suggested Improvements / Gap Analysis."""
    return {
        "SP": ["Secure Software Development Lifecycle", "Zero-Trust Architecture Principles", "Secure Design Patterns"],
        "PR": ["Mastering Network Triage", "Incident Response Playbooks", "Threat Hunting Fundamentals"],
        "AN": ["Threat Intelligence Analysis", "Data Correlation and Pattern Recognition", "Risk Assessment Methods"],
        "CO": ["Collection Operations and Legal Boundaries", "Sensor Deployment and Tuning", "Evidence Handling"],
        "IN": ["Digital Forensics and Evidence Preservation", "Investigation Methodologies", "Legal and Compliance Frameworks"],
        "OM": ["Security Operations Center (SOC) Operations", "Vulnerability Management Lifecycle", "Configuration and Patch Management"],
        "OV": ["Cybersecurity Governance and Risk Management", "Security Program Development", "Third-Party and Supply Chain Risk"],
    }


def _learning_objectives_ja() -> Dict[str, List[str]]:
    """Learning objectives per NICE category (JA)."""
    return {
        "SP": ["セキュアソフトウェア開発ライフサイクル", "ゼロトラストアーキテクチャの原則", "セキュア設計パターン"],
        "PR": ["ネットワークトリアージの習得", "インシデント対応プレイブック", "脅威ハンティングの基礎"],
        "AN": ["脅威インテリジェンス分析", "データ相関とパターン認識", "リスクアセスメント手法"],
        "CO": ["収集運用と法的境界", "センサー展開とチューニング", "証拠取り扱い"],
        "IN": ["デジタルフォレンジックスと証拠保全", "調査方法論", "法とコンプライアンスの枠組み"],
        "OM": ["SOC運用", "脆弱性管理ライフサイクル", "設定とパッチ管理"],
        "OV": ["サイバーセキュリティガバナンスとリスク管理", "セキュリティプログラム開発", "第三者・サプライチェーンリスク"],
    }


def _learning_objectives_zh_tw() -> Dict[str, List[str]]:
    """Learning objectives per NICE category (ZH-TW)."""
    return {
        "SP": ["安全軟體開發生命週期", "零信任架構原則", "安全設計模式"],
        "PR": ["網路分流檢傷精熟", "事件應變劇本", "威脅狩獵基礎"],
        "AN": ["威脅情資分析", "資料關聯與模式辨識", "風險評估方法"],
        "CO": ["蒐集作業與法律邊界", "感測器部署與調校", "證據處理"],
        "IN": ["數位鑑識與證據保全", "調查方法論", "法律與合規架構"],
        "OM": ["資安維運中心（SOC）作業", "弱點管理生命週期", "設定與修補管理"],
        "OV": ["資安治理與風險管理", "安全計畫發展", "第三方與供應鏈風險"],
    }


def _ares_learning_paths_en() -> Dict[str, str]:
    """Project Ares learning path keys → display name (EN)."""
    return {
        "computer_networking": "Computer Networking",
        "network_systems_operations": "Network Systems Operations",
        "endpoint_security": "Endpoint Security",
        "windows_fundamentals": "Windows Fundamentals",
        "intermediate_networking": "Intermediate Networking",
        "intermediate_network_systems_operations": "Intermediate Network Systems Operations",
        "intermediate_endpoint_security": "Intermediate Endpoint Security",
        "advanced_networking": "Advanced Networking",
        "advanced_network_systems_operations": "Advanced Network Systems Operations",
        "advanced_endpoint_security": "Advanced Endpoint Security",
    }


def _ares_learning_paths_ja() -> Dict[str, str]:
    """Project Ares learning path keys → display name (JA). IO-WRL-004 → 学習パス: コンピューターネットワーク."""
    return {
        "computer_networking": "学習パス: コンピューターネットワーク",
        "network_systems_operations": "学習パス: ネットワークシステム運用",
        "endpoint_security": "学習パス: エンドポイントセキュリティ",
        "windows_fundamentals": "学習パス: Windows 基礎",
        "intermediate_networking": "学習パス: 中級ネットワーク",
        "intermediate_network_systems_operations": "学習パス: 中級ネットワークシステム運用",
        "intermediate_endpoint_security": "学習パス: 中級エンドポイントセキュリティ",
        "advanced_networking": "学習パス: 上級ネットワーク",
        "advanced_network_systems_operations": "学習パス: 上級ネットワークシステム運用",
        "advanced_endpoint_security": "学習パス: 上級エンドポイントセキュリティ",
    }


def _ares_learning_paths_zh_tw() -> Dict[str, str]:
    """Project Ares learning path keys → display name (ZH-TW)."""
    return {
        "computer_networking": "學習路徑：電腦網路",
        "network_systems_operations": "學習路徑：網路系統維運",
        "endpoint_security": "學習路徑：端點安全",
        "windows_fundamentals": "學習路徑：Windows 基礎",
        "intermediate_networking": "學習路徑：中級網路",
        "intermediate_network_systems_operations": "學習路徑：中級網路系統維運",
        "intermediate_endpoint_security": "學習路徑：中級端點安全",
        "advanced_networking": "學習路徑：進階網路",
        "advanced_network_systems_operations": "學習路徑：進階網路系統維運",
        "advanced_endpoint_security": "學習路徑：進階端點安全",
    }


def _ares_scenario_titles_en() -> Dict[str, str]:
    """Project Ares scenario ID → display title (EN)."""
    return {
        "BR1": "System Integrator", "BR2": "Network Analyst", "BR5": "Intel Analyst", "BR6": "Linux Basics",
        "BR8": "Network Traffic Analysis", "BR9": "Forensics", "BR10": "Python Scripting Fundamentals",
        "BR11": "System Security Analyst", "BR21": "PowerShell Fundamentals",
        "BR1001": "Windows Fundamentals 1: File System", "BR1002": "Windows Fundamentals 2: Services",
        "BR1003": "Windows Fundamentals 3: Registry", "BR1004": "Windows Fundamentals 4: Networking",
        "M1E": "Disable Botnet", "M2E": "Stop Terrorist Financing", "M3E": "Intercept Attack Plans",
        "M4E": "Stop Malicious Processes", "M5E": "Protect Financial Institution", "M8E": "Defend ICS/SCADA System",
        "M9E": "Manipulate Industrial Control System", "M10E": "Ransomware",
    }


def _ares_scenario_titles_ja() -> Dict[str, str]:
    """Project Ares scenario ID → display title (JA). PD-WRL-003 → ミッション 10 - ランサムウェア."""
    return {
        "BR1": "システムインテグレーター", "BR2": "ネットワークアナリスト", "BR5": "インテルアナリスト", "BR6": "Linux 基礎",
        "BR8": "ネットワークトラフィック分析", "BR9": "フォレンジックス", "BR10": "Python スクリプト基礎",
        "BR11": "システムセキュリティアナリスト", "BR21": "PowerShell 基礎",
        "BR1001": "Windows 基礎 1: ファイルシステム", "BR1002": "Windows 基礎 2: サービス",
        "BR1003": "Windows 基礎 3: レジストリ", "BR1004": "Windows 基礎 4: ネットワーク",
        "M1E": "ボットネット無効化", "M2E": "テロ資金供与の阻止", "M3E": "攻撃計画の傍受",
        "M4E": "悪意あるプロセスの停止", "M5E": "金融機関の保護", "M8E": "ICS/SCADA システムの防御",
        "M9E": "産業用制御システムの操作", "M10E": "ミッション 10 - ランサムウェア",
    }


def _ares_scenario_titles_zh_tw() -> Dict[str, str]:
    """Project Ares scenario ID → display title (ZH-TW)."""
    return {
        "BR1": "系統整合", "BR2": "網路分析師", "BR5": "情資分析師", "BR6": "Linux 基礎",
        "BR8": "網路流量分析", "BR9": "鑑識", "BR10": "Python 腳本基礎",
        "BR11": "系統安全分析師", "BR21": "PowerShell 基礎",
        "BR1001": "Windows 基礎 1：檔案系統", "BR1002": "Windows 基礎 2：服務",
        "BR1003": "Windows 基礎 3：登錄檔", "BR1004": "Windows 基礎 4：網路",
        "M1E": "停用殭屍網路", "M2E": "阻止恐怖主義融資", "M3E": "攔截攻擊計畫",
        "M4E": "停止惡意程序", "M5E": "保護金融機構", "M8E": "防禦 ICS/SCADA 系統",
        "M9E": "操縱工業控制系統", "M10E": "任務 10 - 勒索軟體",
    }


# Unified global translation map: single source for all UI, radar labels, work roles, learning objectives, and Project Ares
LANG_MAP: Dict[str, Dict[str, Any]] = {
    "en": {
        "ui": _ui_en(),
        "categories": {
            "SP": "Securely Provision",
            "PR": "Protect & Defend",
            "AN": "Analyze",
            "CO": "Collect & Operate",
            "IN": "Investigate",
            "OM": "Operate & Maintain",
            "OV": "Oversee & Govern",
        },
        "roles": _roles_en(),
        "learning_objectives": _learning_objectives_en(),
        "ares": {
            "learning_paths": _ares_learning_paths_en(),
            "scenario_titles": _ares_scenario_titles_en(),
        },
    },
    "ja": {
        "ui": _ui_ja(),
        "categories": {
            "SP": "安全に提供",
            "PR": "保護・防御",
            "AN": "分析",
            "CO": "収集・運用",
            "IN": "調査",
            "OM": "運用・維持",
            "OV": "監督・統治",
        },
        "roles": _roles_ja(),
        "learning_objectives": _learning_objectives_ja(),
        "ares": {
            "learning_paths": _ares_learning_paths_ja(),
            "scenario_titles": _ares_scenario_titles_ja(),
        },
    },
    "zh_tw": {
        "ui": _ui_zh_tw(),
        "categories": {
            "SP": "安全維運",
            "PR": "保護與防禦",
            "AN": "分析",
            "CO": "蒐集與營運",
            "IN": "調查",
            "OM": "營運與維護",
            "OV": "監督與治理",
        },
        "roles": _roles_zh_tw(),
        "learning_objectives": _learning_objectives_zh_tw(),
        "ares": {
            "learning_paths": _ares_learning_paths_zh_tw(),
            "scenario_titles": _ares_scenario_titles_zh_tw(),
        },
    },
}


def get_ui(lang: str) -> Dict[str, str]:
    """Return UI strings for the given language. Falls back to English if unknown."""
    if lang not in LANG_MAP:
        lang = "en"
    return LANG_MAP[lang]["ui"]


def get_category_labels(lang: str) -> Dict[str, str]:
    """Radar chart axis labels (e.g. 'Analyze' → '分析'). From LANG_MAP."""
    if lang not in LANG_MAP:
        lang = "en"
    return dict(LANG_MAP[lang]["categories"])


def get_role_display(lang: str, role_id: str) -> Optional[Dict[str, str]]:
    """Translated work role: title, definition, strengths, category. From LANG_MAP."""
    if lang not in LANG_MAP:
        lang = "en"
    return LANG_MAP[lang]["roles"].get(role_id)


def get_learning_objectives(lang: str) -> Dict[str, List[str]]:
    """Learning objectives per NICE category for Suggested Improvements / Gap Analysis. From LANG_MAP."""
    if lang not in LANG_MAP:
        lang = "en"
    return dict(LANG_MAP[lang].get("learning_objectives", _learning_objectives_en()))


def get_ares_learning_path(lang: str, path_key: str) -> str:
    """Localized Project Ares learning path name. path_key e.g. 'computer_networking', 'advanced_networking'."""
    if lang not in LANG_MAP:
        lang = "en"
    ares = LANG_MAP[lang].get("ares", {})
    paths = ares.get("learning_paths", _ares_learning_paths_en())
    return paths.get(path_key, path_key.replace("_", " ").title())


def get_ares_scenario_title(lang: str, scenario_id: str) -> str:
    """Localized Project Ares Battle Room / Mission title. scenario_id e.g. 'BR8', 'M10E'."""
    if lang not in LANG_MAP:
        lang = "en"
    ares = LANG_MAP[lang].get("ares", {})
    titles = ares.get("scenario_titles", _ares_scenario_titles_en())
    return titles.get(scenario_id, scenario_id)
