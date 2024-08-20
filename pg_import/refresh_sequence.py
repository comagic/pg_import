def refresh_sequence(out_file):
    out_file.write('''
    do language plpgsql $$
    declare
      r record;
      t integer;
      s integer;
    begin
      for r in
        select dep.deptype, cl.relname, att.attname, nsc.nspname,
               seq.relname as seqname, nss.nspname as seqnsp
          from pg_class seq
          join pg_namespace nss ON seq.relnamespace = nss.oid
          join pg_depend dep on dep.objid = seq.oid
          join pg_class cl ON dep.refobjid = cl.oid
          join pg_attribute att ON dep.refobjid=att.attrelid AND
                dep.refobjsubid=att.attnum
          join pg_namespace nsc ON cl.relnamespace=nsc.oid
         where seq.relkind = 'S' and deptype = 'a'
      loop
        execute format('select coalesce(max(%I), 0)
                          from %I.%I',
                       r.attname, r.nspname, r.relname) into t;
        execute format('select last_value - (not is_called)::int
                          from %I.%I',
                       r.seqnsp, r.seqname) into s;

        if t <> s then
          perform setval(r.seqnsp ||'.'||r.seqname, t, true);
        end if;
      end loop;
    end;$$;
    ''')
