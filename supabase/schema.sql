create table organizations (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  created_at timestamptz default now()
);

create table profiles (
  id uuid primary key references auth.users(id) on delete cascade,
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

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.profiles (id, email, full_name)
  values (new.id, new.email, coalesce(new.raw_user_meta_data->>'full_name', ''));
  return new;
end;
$$;

create trigger on_auth_user_created
after insert on auth.users
for each row execute procedure public.handle_new_user();

alter table profiles enable row level security;
alter table documents enable row level security;
alter table document_versions enable row level security;
alter table ai_usage_logs enable row level security;

create policy profiles_select_own on profiles for select using (id = auth.uid());
create policy profiles_insert_own on profiles for insert with check (id = auth.uid());
create policy profiles_update_own on profiles for update using (id = auth.uid());

create policy documents_select_own on documents for select using (owner_id = auth.uid());
create policy documents_insert_own on documents for insert with check (owner_id = auth.uid());
create policy documents_update_own on documents for update using (owner_id = auth.uid());
create policy documents_delete_own on documents for delete using (owner_id = auth.uid());

create policy versions_select_own on document_versions for select using (
  exists (select 1 from documents where documents.id = document_versions.document_id and documents.owner_id = auth.uid())
);

create policy usage_select_own on ai_usage_logs for select using (user_id = auth.uid());
create policy usage_insert_own on ai_usage_logs for insert with check (user_id = auth.uid());
