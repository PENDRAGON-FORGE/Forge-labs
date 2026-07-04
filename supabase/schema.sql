create table organizations (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  created_at timestamptz default now()
);

create table profiles (
  id uuid primary key,
  organization_id uuid references organizations(id),
  email text,
  full_name text,
  created_at timestamptz default now()
);

create table projects (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id),
  name text not null,
  created_at timestamptz default now()
);

create table documents (
  id uuid primary key default gen_random_uuid(),
  project_id uuid references projects(id),
  owner_id uuid references profiles(id),
  title text not null,
  template text,
  content text,
  status text default 'draft',
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table document_versions (
  id uuid primary key default gen_random_uuid(),
  document_id uuid references documents(id),
  content text not null,
  created_at timestamptz default now()
);

create table ai_usage_logs (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id),
  user_id uuid references profiles(id),
  provider text,
  task_type text,
  credits_used integer default 0,
  created_at timestamptz default now()
);
