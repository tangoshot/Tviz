class TvizSongInterface(Song):
    name = None
    filename = None
    key = None
    genre = None
    orchestra = None
    singers = []

    def __str__(self):
       
        def safeattr(self, attr):
            try:
                f= getattr(self, attr)
                return f()
            except:
                return '## missing: {s} ##'.format(s=attr)
        
        name= safeattr(self, 'getName')
        genre= safeattr(self, 'getGenre')
        orchestra= safeattr(self, 'getOrchestra')
        singers= safeattr(self, 'getSingers')
        key = safeattr(self, 'getKey')
        
        txt = [
        '''
        {n} ({k})
          orchestra: {o}
          genre: {g}
          singers: {s}
        '''.format(n=name, k=key, o=orchestra, g=genre, s=str(singers))]
        
        txt.append('  tags: ')
        for field in self._fields:
            txt.append('    {f}: {v}'.format(f=field, v=self._fields[field]))
        return '\n'.join(txt)
        
