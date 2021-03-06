#feature.py is a module of HunTag. The Feature class is used for representing a feature type and calculating its value for some input. Feature instances are created by the getFeatureSet function in huntag.py.
from lexicon import Lexicon
import sys

import features

class Feature():
    def __init__(self, kind, name, actionName, fields, radius, cutoff, options ) :
        self.name = name
        self.kind = kind
        self.actionName = actionName
        self.fields = fields
        self.radius = int(radius)
        self.cutoff = int(cutoff)
        self.options = options
        if kind=="lex" :
            if self.options != {}:
                sys.stderr.write('Lexicon features do not yet support options')
                sys.exit(-1)
            self.lexicon = Lexicon(actionName)
        elif kind in ("token","sentence") :
            if actionName not in features.__dict__:
                sys.stderr.write( "Unknown operator named "+actionName+"\n" )
                sys.exit(-1)
            self.function = features.__dict__[actionName]
        else :
            assert False

    def evalSentence_Token(self, sentence) :
        featVec = []
        for pos,word in enumerate(sentence) :
            fieldVec = [ word[field] for field in self.fields ]
            if self.options!={}:
                fieldVec += [self.options]
            feat = self.function( *fieldVec )
            featVec.append(feat)
        return featVec

    def evalSentence_Lex(self, sentence) :
        
        assert len(self.fields)==1
        field = self.fields[0]
        
        wordList = [ word[field] for word in sentence ] 
        
        return self.lexicon.lexEvalSentence(wordList)
        
    def evalSentence_Sentence(self, sentence) :
        if self.options == {}:
            return self.function( sentence, self.fields )        
        else:
            #print; '@'
            return self.function( sentence, self.fields, self.options )        

    def evalSentence(self, sentence) :
        if self.kind=="token" :
            featVec = self.evalSentence_Token(sentence)
        elif self.kind=="lex" :
            featVec = self.evalSentence_Lex(sentence)
        elif self.kind=="sentence" :
            featVec = self.evalSentence_Sentence(sentence)

        return self.multiplyFeatures(sentence, featVec)

    def multiplyFeatures(self, sentence, featVec):
        multipliedFeatVec = []
        for c,word in enumerate(sentence):
            multipliedFeatVec.append([])
            for i in range (-self.radius, self.radius+1):
                pos = c+i
                if pos<0 or pos>len(sentence)-1 :
            	    continue
                
                currentWordFeatures = [feat for feat in featVec[pos] if feat!=0]
                for feat in currentWordFeatures :
                    multipliedFeatVec[c].append(str(i)+'_'+self.name+'='+str(feat))
                        
        return multipliedFeatVec

