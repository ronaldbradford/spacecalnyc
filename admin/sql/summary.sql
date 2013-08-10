SELECT source,MIN(start),MAX(end),COUNT(*) FROM schedule GROUP BY source;
