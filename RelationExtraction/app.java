import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.parser.nndep.DependencyParser;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;
import edu.stanford.nlp.trees.GrammaticalStructure;
import edu.stanford.nlp.trees.TypedDependency;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringReader;
import java.util.List;

public class App {
	public static void main(String[] args) {

		String modelPath = DependencyParser.DEFAULT_MODEL;
		String taggerPath = "edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger";

		try (BufferedReader br = new BufferedReader(
				new FileReader("dataset/dataset.sentences"))) {
			String sentence;
			
			PrintWriter writer = new PrintWriter("dep_parsed.sentences", "UTF-8");
			MaxentTagger tagger = new MaxentTagger(taggerPath);
			DependencyParser parser = DependencyParser.loadFromModelFile(modelPath);
			while ((sentence = br.readLine()) != null) {

				DocumentPreprocessor tokenizer = new DocumentPreprocessor(new StringReader(sentence));
				
				for (List<HasWord> s : tokenizer) {
					List<TaggedWord> tagged = tagger.tagSentence(s);
					GrammaticalStructure gs = parser.predict(tagged);
					String rootWord = "";
					for (TypedDependency tp : gs.allTypedDependencies()) {
						if (tp.gov().toString().equals("ROOT")) {
							rootWord = tp.dep().toString().split("/")[0];
						}
	
					}
					
					boolean isX1DirectlyConnectedToRoot = false;
					boolean isX2DirectlyConnectedToRoot = false;
					
					for (TypedDependency tp : gs.allTypedDependencies()) {
						if ( (tp.gov().toString().contains("PROTX1") && tp.dep().toString().contains(rootWord)) 
								||
							 (tp.gov().toString().contains(rootWord) && tp.dep().toString().contains("PROTX1"))) {
							isX1DirectlyConnectedToRoot = true;
						}
						
						if ( (tp.gov().toString().contains("PROTX2") && tp.dep().toString().contains(rootWord)) 
								||
							 (tp.gov().toString().contains(rootWord) && tp.dep().toString().contains("PROTX2"))) {
							isX2DirectlyConnectedToRoot = true;
						}
						
					}

					int result = 0;
					if (isX1DirectlyConnectedToRoot && isX2DirectlyConnectedToRoot) {
						result = 1;
					}
					writer.println(sentence + "|||" + result);
					System.out.println(".");
				}
			}
			writer.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}

