-- ============================================================
--  인생관리시스템 — Supabase 스키마 복구용 SQL
--  근거: index.html 쿼리 분석 + backup/*.csv 헤더 (2026-08-14)
--  작성일: 2026-09-21
--
--  ⚠️  주의사항
--  1. 이 파일을 실행만 하고 데이터를 직접 수정하지 마세요.
--  2. RLS 정책은 개발 편의를 위해 allow-all로 설정되어 있습니다.
--     운영 환경에서는 user_id = auth.uid() 조건으로 교체하세요.
--  3. reflections 테이블은 원래 요청 목록(13개)에 없었으나
--     index.html에서 광범위하게 사용되므로 포함했습니다.
--  4. monthly_plans에는 코드와 기존 주석 모두에 user_id가 없습니다.
--     현재 앱은 단일 사용자를 가정한 것으로 보입니다.
--     다중 사용자 지원이 필요하면 user_id 컬럼 추가 후 PK 변경 필요.
-- ============================================================

-- ─────────────────────────────────────────
-- 0. 확장 (UUID 자동생성용)
-- ─────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS "pgcrypto";


-- ─────────────────────────────────────────
-- 1. todos
--    근거: index.html:3932 insert payload
--          backup/todos_20260814.csv 헤더
--    컬럼: id, category, text, log_date, done,
--           carried_from, completed_at, user_id
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS todos (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID NOT NULL DEFAULT auth.uid() REFERENCES auth.users ON DELETE CASCADE,
  category      TEXT NOT NULL CHECK (category IN ('work','job','growth','personal')),
  text          TEXT NOT NULL,
  log_date      DATE NOT NULL,
  done          BOOLEAN NOT NULL DEFAULT false,
  carried_from  DATE,                          -- 이월된 원래 날짜 (nullable)
  completed_at  TIMESTAMPTZ,                   -- 완료 처리 시각 (nullable)
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE todos ENABLE ROW LEVEL SECURITY;
CREATE POLICY "todos allow all" ON todos FOR ALL USING (true) WITH CHECK (true);


-- ─────────────────────────────────────────
-- 2. routines
--    근거: index.html:3740 insert payload
--          backup/routines_20260814.csv 헤더
--          index.html:6109 .select('id, label, title, name')
--    컬럼: id, user_id, time_of_day, label, title*, name*,
--           sort_order, is_active, month, year, day_type
--    * title, name은 CSV에 없으나 코드 select에 포함됨 (레거시 가능성)
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS routines (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL DEFAULT auth.uid() REFERENCES auth.users ON DELETE CASCADE,
  time_of_day TEXT NOT NULL,                   -- 예: 'morning', 'evening'
  label       TEXT NOT NULL,
  title       TEXT,                            -- 레거시 컬럼 (nullable)
  name        TEXT,                            -- 레거시 컬럼 (nullable)
  sort_order  INT NOT NULL DEFAULT 0,
  is_active   BOOLEAN NOT NULL DEFAULT true,
  month       INT NOT NULL,                    -- 1–12
  year        INT NOT NULL,
  day_type    TEXT NOT NULL DEFAULT 'weekday', -- 'weekday' | 'weekend'
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE routines ENABLE ROW LEVEL SECURITY;
CREATE POLICY "routines allow all" ON routines FOR ALL USING (true) WITH CHECK (true);


-- ─────────────────────────────────────────
-- 3. routine_logs
--    근거: index.html:3832 upsert payload
--          onConflict: 'routine_id,log_date'
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS routine_logs (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL DEFAULT auth.uid() REFERENCES auth.users ON DELETE CASCADE,
  routine_id  UUID NOT NULL REFERENCES routines(id) ON DELETE CASCADE,
  log_date    DATE NOT NULL,
  done        BOOLEAN NOT NULL DEFAULT false,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (routine_id, log_date)
);

ALTER TABLE routine_logs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "routine_logs allow all" ON routine_logs FOR ALL USING (true) WITH CHECK (true);


-- ─────────────────────────────────────────
-- 4. one_things
--    근거: index.html:4487 upsert payload
--          backup/one_things_20260814.csv 헤더
--          onConflict: 'user_id,scope,category,year,month'
--    컬럼: id, user_id, scope, category, text,
--           year, month, result, updated_at
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS one_things (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL DEFAULT auth.uid() REFERENCES auth.users ON DELETE CASCADE,
  scope       TEXT NOT NULL CHECK (scope IN ('yearly','monthly')),
  category    TEXT NOT NULL,                   -- work/job/growth/personal 등
  text        TEXT NOT NULL DEFAULT '',
  year        INT NOT NULL,
  month       INT NOT NULL DEFAULT 0,          -- 연간 원씽은 0
  result      TEXT,                            -- 결과 기록 (nullable)
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (user_id, scope, category, year, month)
);

ALTER TABLE one_things ENABLE ROW LEVEL SECURITY;
CREATE POLICY "one_things allow all" ON one_things FOR ALL USING (true) WITH CHECK (true);


-- ─────────────────────────────────────────
-- 5. daily_one_things
--    근거: index.html:3418 upsert payload
--          backup/daily_one_things_20260814.csv 헤더
--          onConflict: 'user_id,log_date'
--    ⚠️  요청 스펙은 "log_date UNIQUE"이나
--         코드는 (user_id, log_date) 복합 unique 사용 → 코드 우선
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS daily_one_things (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL DEFAULT auth.uid() REFERENCES auth.users ON DELETE CASCADE,
  log_date    DATE NOT NULL,
  text        TEXT NOT NULL DEFAULT '',
  done        BOOLEAN NOT NULL DEFAULT false,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (user_id, log_date)
);

ALTER TABLE daily_one_things ENABLE ROW LEVEL SECURITY;
CREATE POLICY "daily_one_things allow all" ON daily_one_things FOR ALL USING (true) WITH CHECK (true);


-- ─────────────────────────────────────────
-- 6. weekly_one_things
--    근거: index.html:3340 upsert payload
--          backup/weekly_one_things_20260814.csv 헤더
--          onConflict: 'user_id,week_key'
--    ⚠️  요청 스펙은 "week_key UNIQUE"이나
--         코드는 (user_id, week_key) 복합 unique 사용 → 코드 우선
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS weekly_one_things (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL DEFAULT auth.uid() REFERENCES auth.users ON DELETE CASCADE,
  week_key    TEXT NOT NULL,                   -- 예: '2026-23' (연도-ISO 주차)
  text        TEXT NOT NULL DEFAULT '',
  done        BOOLEAN NOT NULL DEFAULT false,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (user_id, week_key)
);

ALTER TABLE weekly_one_things ENABLE ROW LEVEL SECURITY;
CREATE POLICY "weekly_one_things allow all" ON weekly_one_things FOR ALL USING (true) WITH CHECK (true);


-- ─────────────────────────────────────────
-- 7. ai_reviews
--    근거: index.html:6269 insert payload
--          backup/ai_reviews_20260814.csv 헤더
--    ⚠️  CSV에 user_id 없음 — 임포트 시 user_id 수동 지정 필요
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ai_reviews (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL DEFAULT auth.uid() REFERENCES auth.users ON DELETE CASCADE,
  type        TEXT NOT NULL CHECK (type IN ('weekly','monthly','yearly')),
  period      TEXT NOT NULL,                   -- 예: '2026-23', '2026-08', '2026'
  content     TEXT NOT NULL,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE ai_reviews ENABLE ROW LEVEL SECURITY;
CREATE POLICY "ai_reviews allow all" ON ai_reviews FOR ALL USING (true) WITH CHECK (true);


-- ─────────────────────────────────────────
-- 8. learning_notes
--    근거: index.html:3499 insert payload
--          backup/learning_notes_20260814.csv 헤더
--    ⚠️  CSV에 user_id 없음 — 임포트 시 user_id 수동 지정 필요
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS learning_notes (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL DEFAULT auth.uid() REFERENCES auth.users ON DELETE CASCADE,
  log_date    DATE NOT NULL,
  text        TEXT NOT NULL,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE learning_notes ENABLE ROW LEVEL SECURITY;
CREATE POLICY "learning_notes allow all" ON learning_notes FOR ALL USING (true) WITH CHECK (true);


-- ─────────────────────────────────────────
-- 9. learning_reviews
--    근거: index.html:3634 upsert payload
--          onConflict: 'log_date,user_id'
--    ⚠️  요청 스펙은 "log_date PRIMARY KEY"이나
--         코드는 (log_date, user_id) onConflict → 복합 PK 사용
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS learning_reviews (
  user_id     UUID NOT NULL DEFAULT auth.uid() REFERENCES auth.users ON DELETE CASCADE,
  log_date    DATE NOT NULL,
  content     TEXT NOT NULL,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (log_date, user_id)
);

ALTER TABLE learning_reviews ENABLE ROW LEVEL SECURITY;
CREATE POLICY "learning_reviews allow all" ON learning_reviews FOR ALL USING (true) WITH CHECK (true);


-- ─────────────────────────────────────────
-- 10. monthly_plans
--     근거: index.html:2939 코드 주석 원본 스키마
--           index.html:5055 upsert payload
--     ⚠️  코드 전체에서 user_id 사용 없음 — 단일 사용자 가정
--          다중 사용자 필요 시 user_id 추가 + PK 변경 필요
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS monthly_plans (
  plan_year   INT NOT NULL,
  plan_month  INT NOT NULL,
  self_dev    TEXT,
  family      TEXT,
  work        TEXT,
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (plan_year, plan_month)
);

ALTER TABLE monthly_plans ENABLE ROW LEVEL SECURITY;
CREATE POLICY "monthly_plans allow all" ON monthly_plans FOR ALL USING (true) WITH CHECK (true);


-- ─────────────────────────────────────────
-- 11. projects
--     근거: index.html:7339 insert payload
--           index.html:7372 update status
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS projects (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL DEFAULT auth.uid() REFERENCES auth.users ON DELETE CASCADE,
  name        TEXT NOT NULL,
  category    TEXT NOT NULL,                   -- work/job/growth/personal
  status      TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','completed')),
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
CREATE POLICY "projects allow all" ON projects FOR ALL USING (true) WITH CHECK (true);


-- ─────────────────────────────────────────
-- 12. project_todos
--     근거: index.html:7384 insert payload
--           index.html:7404 update completed_at
--           index.html:8305 select (포함 completed_at)
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS project_todos (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id      UUID NOT NULL DEFAULT auth.uid() REFERENCES auth.users ON DELETE CASCADE,
  project_id   UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  text         TEXT NOT NULL,
  done         BOOLEAN NOT NULL DEFAULT false,
  completed_at TIMESTAMPTZ,                    -- nullable
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE project_todos ENABLE ROW LEVEL SECURITY;
CREATE POLICY "project_todos allow all" ON project_todos FOR ALL USING (true) WITH CHECK (true);


-- ─────────────────────────────────────────
-- 13. recurring_tasks
--     근거: index.html:7897 insert payload
--           index.html:7776 select 컬럼 목록
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS recurring_tasks (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID NOT NULL DEFAULT auth.uid() REFERENCES auth.users ON DELETE CASCADE,
  category    TEXT NOT NULL CHECK (category IN ('work','job','growth','personal')),
  text        TEXT NOT NULL,
  cycle       TEXT NOT NULL,                   -- 예: 'daily', 'weekly:mon,wed,fri'
  start_date  DATE,
  end_date    DATE,                            -- nullable (무기한이면 NULL)
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE recurring_tasks ENABLE ROW LEVEL SECURITY;
CREATE POLICY "recurring_tasks allow all" ON recurring_tasks FOR ALL USING (true) WITH CHECK (true);


-- ─────────────────────────────────────────
-- 14. reflections  ← 요청 목록에 없었으나 앱 필수
--     근거: index.html:4037 upsert payload
--           onConflict: 'log_date,user_id'
--     사용: 오늘의 성찰(기분/잘한것/아쉬운것/내일목표)
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS reflections (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID NOT NULL DEFAULT auth.uid() REFERENCES auth.users ON DELETE CASCADE,
  log_date      DATE NOT NULL,
  mood          TEXT,
  good_things   TEXT,
  regrets       TEXT,
  tomorrow_goal TEXT,
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (log_date, user_id)
);

ALTER TABLE reflections ENABLE ROW LEVEL SECURITY;
CREATE POLICY "reflections allow all" ON reflections FOR ALL USING (true) WITH CHECK (true);
