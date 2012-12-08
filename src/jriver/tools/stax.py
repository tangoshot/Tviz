from tornado.httpclient import HTTPClient
from tviz.http_connection import HttpClient
from jriver.request import JriverRequest
TAG_ERROR_COMMENT = 'errorcomments'
TAG_STACK_TOP = 'Stack Top'
TAG_IS_PROPOGATED = [
    'Singer',
    'Shape',
    'RatingContext',
    'Rating',
    'VersionRating',
    'RatingEnergy',
    'RatingTone',
    'RatingPulse',
    'Tempo',
    'RecVersion',
    'RecDate',        
    'Year',
    'Era',
    'Year',
    'Dj Notes',
    'Lyrics',
    'Milongability',

    'Subgroup',
    'Composer',
    'Orchestra']

TAG_IS_OVERWRITE_STACKTOP = [
    'RatingContext',
    'Rating',
    'VersionRating',
    'RatingEnergy',
    'RatingTone',
    'RatingPulse',
    'Tempo',
    'Shape' ]
         
TAG_IS_SET = [    
    'Singer',
    'Subgroup',
    'Shape']

VALID_STAX_KEYS = [
    'auto',        # without any questions
    'dryrun',   # no changes
    'manual'    # with confirmation questions
]

# LOGIC
# 1. skip values that are consistent in all stack
# 2. if there is a consistent value, propogate to empty values
# 3. TAG_IS_SET should be ordered before consistency check.
# 3. TAG_IS_OVERWRITE_STACKTOP overwrite stack children with the rest

        
def gen_stack_items(client):
    
    # TODO
    # can we have a helper with 
    # call(action=FilesSearch, fields=[...])
    items = client.call(JriverRequest.FilesSearch(fields=['Stack Top']))
    
    # filter items that have a 'Stack Top' field
    items = [item for item in items if 'Stack Top' in item]
    
    stacktops = frozenset([item['Stack Top'] for item in items])
    
    print stacktops
    
    for stacktop in stacktops:
        query = '[Stack Top]=[%s]' % stacktop
        items = client.call(JriverRequest.FilesSearch(query = query))
        
        yield (stacktop, items)

def tag_value(key, tag, items):
    for item in items:
        if item['Key'] != key:
            continue
        
        if tag in item:
            return item[tag]
        else:
            return None
    
    raise Except('Item key not found')
    

def stack_values(tag, stackkey, items):
    '''
    eval stack value candidates
    - 'None' if all stack elements have empty value
    - one if stack elements all agree
    - multiple if there is a conflict. 
    - set values will all be a string seperated by ';'
    - trailing empty spaces are trimmed
    '''
    top_value = tag_value(stackkey, tag, items)

    # if stoptop overwrites and has a value
    if tag in TAG_IS_OVERWRITE_STACKTOP and top_value:
        return set([top_value])
    
    # select all nonempty values
    values = [ x[tag].strip() for x in items if tag in x]
    
    # further normalize if set values
    if tag in TAG_IS_SET:
        values = [normalize_set_values(v) for v in values]
    
    values = set(values)
    
    values = values - set([None])
    
    return values
    
    
def normalize_set_values(values):
    values = values.split(';')
    values = [v.strip() for v in values].sort()
    if values:
        values = ';'.join(values)
    return values




def stack_updates(stack, items):
        for tag in TAG_IS_PROPOGATED:
            values = stack_values(tag, stack, items)
            if len(values) == 0:
                continue
            if len(values) >= 2:
                keys = [i['Key'] for i in items]
                yield dict(type='conflict', tag=tag, keys = keys, values = values)
                continue

            # single consistent stack  value should be propagated
            assert len(values) == 1
            stackval = list(values)[0]
            
            for item in items:
                itemval = item[tag] if tag in item else None
                itemkey = item['Key']
                
                if itemval == stackval:
                    continue
                
                # item value is either empty or a normalized variation of stack value
                yield dict(type='update', key=itemkey, tag=tag, oldval = itemval, newval = stackval)


def print_change_info(param):
    if param['type'] == 'update':
        print u"UPDATE {key}({tag}): {oldval} --> {newval}".format(**param)
        return
    if param['type'] == 'conflict':
        print u"CONFLICT {tag} = {values}  (keys= {keys})".format(**param)
        return
    raise Except('Invalid param type %s' % param['type'])

if __name__ == '__main__':
    client = HttpClient(user= 'mc', pwd= 'mc', port='48105',base='MCWS/v1/')
    for x in gen_stack_items(client):
        stack = x[0]
        items = x[1]
        stacklen = len(x[1])
        
        for s in stack_updates(stack, items):
            print_change_info(s)

# TODO: add assertions. i.e. what needs to be the same, Name, Album etc. create an error log.


#    memberchk(Flag:McWsKey, [auto:true, test:false,confirm:confirm]),
#
#    mcws_write_access(McWsKey),
#    propogated_tags(Tags),
#
#    % generator
#    gen_stack_items(StackKey, StackItems),
#    % ---
#    
#    % generator
#    member(Tag, Tags),
#    
#    succeeds(collect_values(Tag, StackItems, Values)),
#    succeeds(proccess_stack(Tag,StackKey, Values, StackItems)),
#    fail.
#stax(_, _, _):-
#    writef_heading('Report\n'),
#    flag(stax_error_comment, N1, N1),
#    flag(stax_change, N2, N2),
#
#    writef('Error Comments: %t\n', [N1]),
#    writef('Tag Changes:\n %t', [N2]),
#    !.
#    
#
#% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%           Query Stack Items
#% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
#gen_stack_items(TopKey, StackItems):-
#    % start with all stacks instead? by getting all field values??
#    propogated_tags(Tags),
#    gen_stack_items(TopKey, StackItems,Tags).
#    
#gen_stack_items(TopKey, StackItems,Tags):-
#    
#    mcall(search('', ['Stack Top']), 
#        [mpl(_,Items)]),
#    !,
#    
#    findall(X,         
#        (    member(Item,Items), 
#            member('stack top'=X, Item)),
#        TopKeysList),
#    list_to_set(TopKeysList, TopKeys),
#        
#    % mcall(field('Stack Top'), TopKeys),
#    % this does not work for MC16 anymore, but it works for MC17
#    
#    member(TopKey, TopKeys),
#    TopKey\= '-1',
#
#    mcall(search( ['[Stack Top]=[',TopKey,']'], Tags), [mpl(_,StackItems)]).    
#    
#    
#    
#
#    
#    
#% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%           Agregate Stack Values
#% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    
#    
#collect_values(Tag, ItemList, Values):-
#    setofall(Value, 
#        (    member(Item, ItemList),
#            collect_value(Tag, Item, Value)),
#        Values).
#
#collect_value(Tag,Item, NormalizedValue):-
#    unordered_set_tags(Tags),
#    memberchk(Tag, Tags),
#    
#    memberchk(Tag=ItemValue, Item),
#    atomic_list_concat(Values, ;, ItemValue),
#    sort(Values, Values1),
#    atomic_list_concat(Values1, ;, NormalizedValue),
#    !.
#
#collect_value(Tag, Item, Value):-
#    memberchk(Tag= Value, Item),
#    !.
#collect_value(_Tag, _Item, '').
#
#
#write_playlist:-
#    forall(    gen_playlist(_,Key),
#        (    mcall(field(Key, 'filename'), FileName),
#            writef('%t: %t \n',[Key, FileName]))).
#
#
#% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%           Proccess Stack Updates
#% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    
#
#% TODO
#% proccess_stack(Tag, TopKey, Values, Items):-
#%        set_tag()
#
#    
#
#    % writef('.'),flush_output.
#    % stack has consistent value for that field.
#
#proccess_stack(_,_, [_Value], _):- !.
#
#proccess_stack(_,_, Values, _):- 
#    normalize_values(Values, [_Values]),
#    !.
#    
#proccess_stack(Tag, TopKey, Values, StackItems):-
#    consistent_values(Values),
#    % stack has a consistent values. (same up to case, or some empty values)
#    member(Value, Values),
#    Value\= '', % any consistent value except empty should be fine, although stack value could be prefered here when not empty.
#    
#    propogate_value_in_snormalize_valuestack(Tag, TopKey, StackItems, Value),!.
#    
#proccess_stack(Tag,TopKey, Values, StackItems):-
#        resolve_conflict(Tag,TopKey, Values, StackItems).
#        % add something to a custom field, reporting the conflict.
#
#normalize_values(Values, Values1):-
#    setofall(X1, (member(X,Values), downcase_atom(X,X1)), Values1),
#    !.
#
#consistent_values(Values):-
#    normalize_values(Values, Values1),
#    delete(Values1, '', [_Value]),
#    !.
#    
#        
#% =============================
#% Propogate consistent values
#% =============================
#
#propogate_value_in_stack(Tag,StackKey, StackItems, Value):-
#    list_stack_heading(StackKey, StackItems),
#    forall(member(Item, StackItems),
#        propogate_value(Tag, Item, Value)).
#        
#propogate_value(Tag, Item, Value):-
#    memberchk(Tag=Value, Item),
#    % the item already has that value.
#    !.
#
#propogate_value(Tag, Item, Value):-
#    memberchk( key=Key, Item),
#
#    % writef('item(%t) <-- %t(%t)\n',[Key, Tag, Value]),
#    % set_field(Key,Field,Value),
#    set_field(Key, Tag, Value).
#    
#% =============================
#% Resolve conflict
#% =============================
#
#% prefer the stack top value, if so specified for that tag and 
#% if the stack tag has nonempty value.
#% this is usually done for the subjective tags that tend to change over time.
#
#resolve_conflict(Tag, StackKey, _Values, StackItems):-
#
#    prefer_stack_top(Tags),
#    memberchk(Tag, Tags),
#
#    member(TopItem, StackItems),
#    memberchk(key= StackKey, TopItem),
#    memberchk(Tag= TopValue, TopItem),
#
#    list_stack_heading(StackKey, StackItems),
#
#    writef('Overriding stack with top value %t(%t)\n',[Tag, TopValue]),
#    
#    forall(member(Item, StackItems),
#        propogate_value(Tag, Item, TopValue)).
#    
#
#
#resolve_conflict(Tag, StackKey, Values, StackItems):-
#    list_stack_heading(StackKey, StackItems),
#
#    forall(member(Item, StackItems),
#        add_conflict_comment(Tag, Item, Values)),
#    !.
#    
#add_conflict_comment(Tag, Item, _Values):-
#    error_comment_field(Etag),
#    memberchk(key= Key, Item),
#    
#    atomic_list_concat([spe, '/', Tag], IncValue), 
#    
#    (new_item_value(Item, Etag, IncValue, NewValue) ->
#        set_field(Key, Etag, NewValue)
#    ;    true).
#    
#    
#new_item_value(Item, Tag, IncValue,IncValue):-
#    % this may happen when there are conflicting value and a missing value
#    \+ memberchk(Tag= _, Item),
#    !.
#    
#new_item_value(Item, Tag, IncValue,NewValue):-
#    downcase_atom(IncValue, NormalIncValue1),
#    delete(NormalIncValue1, ' ', NormalIncValue),
#    
#    memberchk(Tag= OldValue, Item),
#    downcase_atom(OldValue, NormalOldValue1),
#    delete(NormalOldValue1,' ', NormalOldValue),
#    
#    atomic_list_concat(NormalOldValues, ';',NormalOldValue),
#    
#    \+ memberchk(NormalIncValue, NormalOldValues),
#    atomic_list_concat([IncValue, ';', OldValue], NewValue),
#    write(OldValue + IncValue),nl,
#    write(NormalOldValues + NormalIncValue),nl.
#
#
#    
#    
#% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%            CHANGE LIBRARY
#% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
#set_field(Key, Tag, Value):-
#    sf_document(Key, Tag, Value),
#    flatten([Value], Value1),
#    atomic_list_concat(Value1,Value2),
#    mcall(set_field(Key, Tag, Value2), _),
#    !.
#set_field(Key, Tag, Value):-
#    
#    writef('Error in item(%t) <-- %t(%t)\n',[Key, Tag, Value]),
#    !.
#
#% ------------------------------
#    
#sf_document(_, Tag, _):-
#    error_comment_field(Tag), 
#    flag(stax_error_comment, N, N+1),
#    fail.
#    
#sf_document(_, Tag, _):-
#    \+ error_comment_field(Tag), 
#    flag(stax_change, N, N+1),
#    fail.
#sf_document(Key, _Tag, _Value):-
#    ( mcall(field(Key, name), Name) ->
#        writef('Changing: %t\n',[Name])
#    ;    writef('unknown name\n')),
#    fail.
#sf_document(_,_,_):- !.
#    
#
#% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%           UTIL
#% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
#list_stack_heading(StackKey, StackItems):- 
#    findall(Key, 
#        (    member(StackItem, StackItems), 
#            member(key= Key, StackItem)), 
#        StackKeys),
#    writef_heading('Stack: %t \n',[StackKey]),
#    writef('%t\n',[StackKeys]),
#    write_line,
#    !.
#
#stackbest(Key):-
#    stackof(Key, Key),
#    !.
#
#stackof(Key, StackKey):-
#    stack_top_field(StackTopField),
#    mcall(field(Key, StackTopField), StackTopKey),
#    stackbest(Key, StackTopKey, StackKey).
#    
#stackbest(Key, '-1', Key):- !.
#stackbest(_Key, StackTop, StackTop).
