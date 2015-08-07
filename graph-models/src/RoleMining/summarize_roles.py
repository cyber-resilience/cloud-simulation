#!/usr/bin/env python3

def load_features():
    f_f = open('role_features.txt')
    features = []
    for line in f_f:
        features.append(line.strip())
    f_f.close()
    return features

def get_role_descriptions():
    features = load_features()
    f_d = open('role_description.txt')
    role_descriptions = []
    for line in f_d:
        tokens = line.strip().split('  ')
        role_strengths = []
        for t in tokens:
            role_strengths.append(float(t))
        role_features = []
        for i in range(len(role_strengths)):
            if role_strengths[i] > 0.4:
                role_features.append('high ' + features[i])
        if len(role_features) == 0:
            max = 0
            i = 0
            for val in role_strengths:
                if val > max:
                    max = val
                    role_desc = features[i]        
                i += 1
            role_features.append('high ' + role_desc)
        #print('Role description: ' + ', '.join(role_features))
        role_descriptions.append(', '.join(role_features))
    f_d.close()
    return role_descriptions

def summarize_roles():
    role_descriptions = get_role_descriptions()
    f_d = open('role_distribution.csv')
    f_out = open('roles.csv', 'w')
    i = 0 
    for line in f_d:
        count = line.strip()
        f_out.write(count + '\t' + role_descriptions[i] + '\n')
        i += 1 
    f_d.close()
    f_out.close()

summarize_roles()
