Search.setIndex({"alltitles": {"1. Explicit Dependencies": [[10, "explicit-dependencies"]], "2. Immutable Results": [[10, "immutable-results"]], "3. Minimal Infrastructure": [[10, "minimal-infrastructure"]], "4. Fail Fast, Fail Explicitly": [[10, "fail-fast-fail-explicitly"]], "5. Portable Results": [[10, "portable-results"]], "API": [[11, "api"]], "API Reference": [[5, null]], "Abstract Syntax Tree": [[1, null]], "Abstract Syntax Tree (AST)": [[9, null]], "Access to Parent Steps": [[0, "access-to-parent-steps"]], "Advanced Usage": [[0, null]], "Analysis Inheritance": [[0, "analysis-inheritance"]], "Analysis as Classes": [[10, "analysis-as-classes"]], "Base Class": [[2, null]], "Basic Inheritance": [[0, "basic-inheritance"]], "Best Practices": [[0, "best-practices"]], "Class-Based vs. Functional": [[10, "class-based-vs-functional"]], "Contents": [[11, "contents"]], "Core Principles": [[10, "core-principles"]], "Custom Serialization": [[10, "custom-serialization"]], "Decorator-Based Step Definition": [[10, "decorator-based-step-definition"]], "Defining an Analysis": [[13, "defining-an-analysis"]], "Dependencies": [[13, "dependencies"]], "Dependency Tracking": [[13, "dependency-tracking"]], "Dependency Usage": [[9, "dependency-usage"]], "Design Philosophy": [[10, null]], "Design Tradeoffs": [[10, "design-tradeoffs"]], "Direct Assignments": [[9, "direct-assignments"]], "Example Analysis": [[13, "example-analysis"]], "Executing an Analysis": [[13, "executing-an-analysis"]], "Executor": [[3, null]], "Explicit vs. Implicit": [[10, "explicit-vs-implicit"]], "Flag Setting": [[13, "flag-setting"]], "Future Considerations": [[10, "future-considerations"]], "Graph": [[4, null]], "Implementation Decisions": [[10, "implementation-decisions"]], "Inheritance Features": [[0, "inheritance-features"]], "Installation": [[12, null]], "Key Features": [[11, "key-features"]], "Loading": [[13, "loading"]], "Loading with Original Class Definition": [[13, "loading-with-original-class-definition"]], "Loading without Original Class Definition": [[13, "loading-without-original-class-definition"]], "Metadata": [[6, null]], "Method Overriding": [[0, "method-overriding"]], "Multi-level Inheritance": [[0, "multi-level-inheritance"]], "Mutability": [[13, "mutability"]], "Overview": [[11, "overview"]], "Quick Start": [[13, null]], "Redundant Execution": [[13, "redundant-execution"]], "Results": [[7, null]], "Results Management": [[10, "results-management"]], "Runtime Inference": [[13, "runtime-inference"]], "Saving": [[13, "saving"]], "Saving and Loading Analysis States": [[13, "saving-and-loading-analysis-states"]], "Selective Loading": [[13, "selective-loading"]], "Serialization Approach": [[10, "serialization-approach"]], "Step Decorator": [[8, null], [13, "step-decorator"]], "Step Dependencies": [[0, "step-dependencies"]], "Validations": [[9, "validations"]], "Visualization Support": [[0, "visualization-support"]], "Visualizing Analysis Steps": [[13, "visualizing-analysis-steps"]], "yaflux": [[11, null]]}, "docnames": ["advanced_usage", "api/ast", "api/base", "api/executor", "api/graph", "api/index", "api/metadata", "api/results", "api/step", "ast", "design", "index", "installation", "quick_start"], "envversion": {"sphinx": 64, "sphinx.domains.c": 3, "sphinx.domains.changeset": 1, "sphinx.domains.citation": 1, "sphinx.domains.cpp": 9, "sphinx.domains.index": 1, "sphinx.domains.javascript": 3, "sphinx.domains.math": 2, "sphinx.domains.python": 4, "sphinx.domains.rst": 2, "sphinx.domains.std": 2, "sphinx.ext.intersphinx": 1, "sphinx.ext.viewcode": 1}, "filenames": ["advanced_usage.md", "api/ast.rst", "api/base.rst", "api/executor.rst", "api/graph.rst", "api/index.rst", "api/metadata.rst", "api/results.rst", "api/step.rst", "ast.md", "design.md", "index.md", "installation.md", "quick_start.md"], "indexentries": {"_data (yaflux._results.results attribute)": [[7, "yaflux._results.Results._data", false]], "_metadata (yaflux._results.results attribute)": [[7, "yaflux._results.Results._metadata", false]], "allow_mutation() (yaflux._results.flaglock class method)": [[7, "yaflux._results.FlagLock.allow_mutation", false]], "allow_mutation() (yaflux._results.resultslock class method)": [[7, "yaflux._results.ResultsLock.allow_mutation", false]], "astselfmutationerror": [[1, "yaflux._ast.AstSelfMutationError", false]], "astundeclaredusageerror": [[1, "yaflux._ast.AstUndeclaredUsageError", false]], "available_steps (yaflux._base.base attribute)": [[2, "yaflux._base.Base.available_steps", false]], "available_steps (yaflux._base.base property)": [[2, "id0", false]], "base (class in yaflux._base)": [[2, "yaflux._base.Base", false]], "build_read_graph() (in module yaflux._graph)": [[4, "yaflux._graph.build_read_graph", false]], "build_write_graph() (in module yaflux._graph)": [[4, "yaflux._graph.build_write_graph", false]], "can_mutate() (yaflux._results.flaglock class method)": [[7, "yaflux._results.FlagLock.can_mutate", false]], "can_mutate() (yaflux._results.resultslock class method)": [[7, "yaflux._results.ResultsLock.can_mutate", false]], "can_mutate_key() (yaflux._results.resultslock class method)": [[7, "yaflux._results.ResultsLock.can_mutate_key", false]], "circulardependencyerror": [[4, "yaflux._graph.CircularDependencyError", false]], "completed_steps (yaflux._base.base attribute)": [[2, "yaflux._base.Base.completed_steps", false]], "completed_steps (yaflux._base.base property)": [[2, "id1", false]], "compute_topological_levels() (in module yaflux._graph)": [[4, "yaflux._graph.compute_topological_levels", false]], "creates (in module yaflux._step)": [[8, "yaflux._step.creates", false]], "creates_flags (in module yaflux._step)": [[8, "yaflux._step.creates_flags", false]], "execute() (yaflux._base.base method)": [[2, "yaflux._base.Base.execute", false]], "execute_all() (yaflux._base.base method)": [[2, "yaflux._base.Base.execute_all", false]], "flagerror": [[7, "yaflux._results.FlagError", false]], "flaglock (class in yaflux._results)": [[7, "yaflux._results.FlagLock", false]], "get_mutable_keys() (yaflux._results.resultslock class method)": [[7, "yaflux._results.ResultsLock.get_mutable_keys", false]], "get_step_info() (yaflux._base.base method)": [[2, "yaflux._base.Base.get_step_info", false]], "get_step_metadata() (yaflux._base.base method)": [[2, "yaflux._base.Base.get_step_metadata", false]], "get_step_metadata() (yaflux._results.results method)": [[7, "yaflux._results.Results.get_step_metadata", false]], "get_step_results() (yaflux._base.base method)": [[2, "yaflux._base.Base.get_step_results", false]], "get_step_results() (yaflux._results.results method)": [[7, "yaflux._results.Results.get_step_results", false]], "load() (yaflux._base.base class method)": [[2, "yaflux._base.Base.load", false]], "metadata_report() (yaflux._base.base method)": [[2, "yaflux._base.Base.metadata_report", false]], "module": [[1, "module-yaflux._ast", false], [2, "module-yaflux._base", false], [4, "module-yaflux._graph", false], [7, "module-yaflux._results", false], [8, "module-yaflux._step", false]], "mutabilityconflicterror": [[4, "yaflux._graph.MutabilityConflictError", false]], "mutates (in module yaflux._step)": [[8, "yaflux._step.mutates", false]], "requires (in module yaflux._step)": [[8, "yaflux._step.requires", false]], "requires_flags (in module yaflux._step)": [[8, "yaflux._step.requires_flags", false]], "results (class in yaflux._results)": [[7, "yaflux._results.Results", false]], "results (yaflux._base.base attribute)": [[2, "yaflux._base.Base.results", false]], "results (yaflux._base.base property)": [[2, "id2", false]], "resultslock (class in yaflux._results)": [[7, "yaflux._results.ResultsLock", false]], "save() (yaflux._base.base method)": [[2, "yaflux._base.Base.save", false]], "set_metadata() (yaflux._results.results method)": [[7, "yaflux._results.Results.set_metadata", false]], "step() (in module yaflux._step)": [[8, "yaflux._step.step", false]], "unauthorizedmutationerror": [[7, "yaflux._results.UnauthorizedMutationError", false]], "validate_ast() (in module yaflux._ast)": [[1, "yaflux._ast.validate_ast", false]], "validate_incompatible_mutability() (in module yaflux._graph)": [[4, "yaflux._graph.validate_incompatible_mutability", false]], "visualize_dependencies() (yaflux._base.base method)": [[2, "yaflux._base.Base.visualize_dependencies", false]], "yaflux._ast": [[1, "module-yaflux._ast", false]], "yaflux._base": [[2, "module-yaflux._base", false]], "yaflux._graph": [[4, "module-yaflux._graph", false]], "yaflux._results": [[7, "module-yaflux._results", false]], "yaflux._step": [[8, "module-yaflux._step", false]]}, "objects": {"": [[8, 0, 1, "", "creates"], [8, 0, 1, "", "creates_flags"], [8, 0, 1, "", "mutates"], [8, 0, 1, "", "requires"], [8, 0, 1, "", "requires_flags"]], "yaflux": [[1, 1, 0, "-", "_ast"], [2, 1, 0, "-", "_base"], [4, 1, 0, "-", "_graph"], [6, 1, 0, "-", "_metadata"], [7, 1, 0, "-", "_results"], [8, 1, 0, "-", "_step"]], "yaflux._ast": [[1, 2, 1, "", "AstSelfMutationError"], [1, 2, 1, "", "AstUndeclaredUsageError"], [1, 3, 1, "", "validate_ast"]], "yaflux._base": [[2, 4, 1, "", "Base"]], "yaflux._base.Base": [[2, 5, 1, "id0", "available_steps"], [2, 5, 1, "id1", "completed_steps"], [2, 6, 1, "", "execute"], [2, 6, 1, "", "execute_all"], [2, 6, 1, "", "get_step_info"], [2, 6, 1, "", "get_step_metadata"], [2, 6, 1, "", "get_step_results"], [2, 6, 1, "", "load"], [2, 6, 1, "", "metadata_report"], [2, 5, 1, "id2", "results"], [2, 6, 1, "", "save"], [2, 6, 1, "", "visualize_dependencies"]], "yaflux._graph": [[4, 2, 1, "", "CircularDependencyError"], [4, 2, 1, "", "MutabilityConflictError"], [4, 3, 1, "", "build_read_graph"], [4, 3, 1, "", "build_write_graph"], [4, 3, 1, "", "compute_topological_levels"], [4, 3, 1, "", "validate_incompatible_mutability"]], "yaflux._metadata": [[6, 4, 1, "", "Metadata"]], "yaflux._metadata.Metadata": [[6, 0, 1, "", "args"], [6, 0, 1, "", "creates"], [6, 0, 1, "", "elapsed"], [6, 0, 1, "", "kwargs"], [6, 0, 1, "", "requires"], [6, 0, 1, "", "timestamp"], [6, 6, 1, "", "to_dict"]], "yaflux._results": [[7, 2, 1, "", "FlagError"], [7, 4, 1, "", "FlagLock"], [7, 4, 1, "", "Results"], [7, 4, 1, "", "ResultsLock"], [7, 2, 1, "", "UnauthorizedMutationError"]], "yaflux._results.FlagLock": [[7, 6, 1, "", "allow_mutation"], [7, 6, 1, "", "can_mutate"]], "yaflux._results.Results": [[7, 0, 1, "", "_data"], [7, 0, 1, "", "_metadata"], [7, 6, 1, "", "get_step_metadata"], [7, 6, 1, "", "get_step_results"], [7, 6, 1, "", "set_metadata"]], "yaflux._results.ResultsLock": [[7, 6, 1, "", "allow_mutation"], [7, 6, 1, "", "can_mutate"], [7, 6, 1, "", "can_mutate_key"], [7, 6, 1, "", "get_mutable_keys"]], "yaflux._step": [[8, 0, 1, "", "creates"], [8, 0, 1, "", "creates_flags"], [8, 0, 1, "", "mutates"], [8, 0, 1, "", "requires"], [8, 0, 1, "", "requires_flags"], [8, 3, 1, "", "step"]]}, "objnames": {"0": ["py", "attribute", "Python attribute"], "1": ["py", "module", "Python module"], "2": ["py", "exception", "Python exception"], "3": ["py", "function", "Python function"], "4": ["py", "class", "Python class"], "5": ["py", "property", "Python property"], "6": ["py", "method", "Python method"]}, "objtypes": {"0": "py:attribute", "1": "py:module", "2": "py:exception", "3": "py:function", "4": "py:class", "5": "py:property", "6": "py:method"}, "terms": {"": [0, 1, 4, 10, 13], "0": [4, 13], "1": [0, 4, 13], "10": [0, 13], "100": [0, 13], "11": [], "2": [0, 9, 13], "20": 13, "3": 13, "30": 13, "4": 13, "42": [], "90": 13, "A": [0, 4, 9, 11, 13], "As": 13, "For": [2, 9, 12], "If": [2, 7, 13], "In": [9, 13], "It": [9, 11, 13], "Not": 10, "One": [0, 9, 10, 13], "Or": [12, 13], "The": [0, 2, 7, 10, 13], "There": 13, "These": [0, 10, 13], "To": 13, "__init__": 0, "_ast": 1, "_base": 2, "_data": [7, 10], "_flag_b": 13, "_flag_c": 13, "_graph": 4, "_mark": 13, "_metadata": [6, 7, 10], "_mut_data": 13, "_mutated_data": 13, "_portabl": [], "_result": 7, "_step": 8, "abil": [9, 10, 13], "about": [2, 9, 10], "abov": 13, "abstract": [5, 11], "accept": 10, "access": [10, 13], "accident": 10, "achiev": 10, "across": [0, 10], "actual": [], "ad": [10, 13], "add": 10, "addit": [10, 12], "adjac": 4, "advanc": 11, "advanced_result": 0, "advanced_step": 0, "advancedanalysi": 0, "advantag": 13, "again": 13, "against": 10, "agnost": 10, "aim": 10, "alias_data": 9, "all": [0, 2, 7, 9, 10, 13], "allow": [0, 7, 9, 10, 13], "allow_mut": 7, "alreadi": 7, "also": [9, 10, 13], "altern": 10, "alwai": 0, "an": [0, 1, 2, 4, 9, 10, 11], "analys": [0, 10, 13], "analysi": [2, 4, 7, 8, 9, 11], "analyt": [10, 11, 13], "ani": [2, 4, 7, 9, 10, 13], "appear": 0, "approach": [11, 13], "ar": [0, 4, 9, 10, 11, 13], "arbitrari": 10, "architectur": 10, "archiv": 2, "arg": 6, "argument": 13, "around": [10, 13], "assert": 13, "assum": 13, "ast": [1, 11], "astselfmutationerror": [1, 5, 9], "astundeclaredusageerror": [1, 5, 9], "attempt": [2, 7, 13], "attribut": [2, 10], "automat": [10, 11, 13], "avail": [2, 10], "available_step": [0, 2, 13], "avoid": 0, "b": [0, 4], "backward": 10, "base": [0, 1, 4, 5, 6, 7, 9, 11, 12, 13], "base_data": 0, "baseanalysi": 0, "bash": [], "becaus": [9, 10, 13], "been": [7, 13], "befor": [9, 10], "behavior": [0, 9], "being": 9, "benefit": [9, 10, 13], "better": 10, "between": [0, 10, 11, 13], "boilerpl": 10, "bool": [2, 7], "both": [4, 10, 13], "boundari": 0, "break": 13, "build": [0, 4], "build_read_graph": [4, 5], "build_write_graph": [4, 5], "built": [10, 11, 13], "bypass": 9, "c": [], "call": 0, "callabl": 8, "can": [0, 7, 9, 10, 11, 12, 13], "can_mut": 7, "can_mutate_kei": 7, "capabl": 10, "case": [9, 10, 13], "catch": [9, 10], "central": 10, "challeng": [10, 13], "chang": [10, 13], "characterist": 9, "cheap": 10, "check": [1, 7, 9, 10], "child": 0, "choic": 10, "choos": 10, "circulardependencyerror": [4, 5], "cl": 7, "class": [0, 5, 6, 7, 9, 11], "classmethod": [2, 7], "clean": 10, "clean_data": [], "cleanedanalysi": [], "cleaner": 10, "clear": [0, 2, 10, 11, 13], "clearer": 10, "code": [9, 10], "codebas": 10, "color": [], "combin": [10, 13], "come": 0, "common": 0, "compat": 10, "compil": 9, "complet": [0, 2, 11, 13], "complete_fillcolor": [], "complete_linecolor": [], "completed_step": [0, 2, 13], "complex": [0, 10, 11, 13], "complexanalysi": 0, "compon": [9, 13], "compress": 10, "compromis": 10, "comput": [4, 10], "compute_topological_level": [4, 5], "concern": 10, "concreteanalysi": [], "configur": 2, "conflict": [0, 4], "consid": 9, "consider": 11, "consist": [0, 10], "constructor": [], "contain": [6, 7], "context": 7, "control": 7, "core": 11, "correct": [9, 13], "correctli": 13, "creat": [0, 2, 6, 7, 8, 9, 10, 13], "create_plot": [], "creates_flag": 8, "cross": 0, "crucial": 9, "current": [2, 7, 13], "custom": [0, 13], "customanalysi": 0, "d": 13, "dag": 13, "darkgreen": [], "data": [0, 6, 7, 10, 11], "dataanalysi": [], "debug": 10, "decis": 11, "declar": [0, 9, 10, 11], "decor": [5, 7, 9, 11], "def": [0, 9, 10, 13], "default": [2, 10, 13], "defin": [0, 2, 11], "definit": [7, 9, 11], "depdend": 13, "depend": [2, 4, 11, 12], "describ": 10, "design": [0, 11], "develop": [9, 10], "dict": [2, 4, 6, 7], "digraph": 2, "direct": [10, 13], "directli": [0, 9], "disambigu": 13, "discourag": 10, "do": 13, "docstr": 0, "document": [0, 10], "doe": [9, 13], "doesn": 10, "done": 13, "dot": [], "downstream": 13, "drop": [], "dynam": 7, "e": [9, 13], "each": [4, 7, 10, 13], "earli": [9, 10], "easi": 10, "easier": 10, "easili": 13, "edg": 4, "effect": [9, 10, 13], "effici": [10, 13], "elaps": 6, "enabl": 10, "encapsul": 10, "encourag": 10, "end": [2, 13], "enforc": 10, "enhanc": 10, "ensur": [9, 10, 11, 13], "entir": [10, 13], "error": [9, 10, 13], "essenti": 11, "evalu": 9, "even": [0, 10], "exampl": [0, 9], "except": [1, 4, 7, 9, 13], "exclud": [2, 13], "execut": [2, 10, 11], "execute_al": 2, "executor": [5, 11], "exist": [2, 10], "explicitli": [0, 9, 11], "extend": [0, 10], "extendedanalysi": 0, "extens": [0, 10], "extern": [10, 12], "extra": 12, "extract_featur": [], "facilit": 10, "fail": [9, 13], "fals": 2, "familiar": 10, "featur": [9, 10, 12, 13], "featureanalysi": [], "feedback": [9, 10], "file": [2, 10, 13], "filepath": 2, "fill": [], "final": [0, 13], "final_data": 13, "final_step": 0, "first": [0, 2, 13], "fix": [6, 13], "flag": [4, 7, 8, 10], "flagerror": [5, 7], "flaglock": [5, 7], "float": 6, "focu": 13, "follow": [9, 10, 13], "font": [], "fontnam": [], "fontsiz": [], "forc": [2, 10, 13], "format": [2, 10], "framework": [2, 9, 10, 11], "from": [0, 2, 9, 11, 13], "from_analysi": [], "full": [10, 12, 13], "func": 1, "func_nam": 1, "function": [0, 1, 13], "fundament": 10, "futur": 11, "gener": 13, "get": [0, 2, 7, 13], "get_mutable_kei": 7, "get_step_info": 2, "get_step_metadata": [2, 7], "get_step_result": [2, 7], "granular": 7, "graph": [0, 2, 5, 11, 13], "graphconfig": 2, "graphviz": 2, "gray70": [], "guarante": 9, "guid": [10, 13], "gzip": 10, "ha": [7, 10, 13], "handl": [10, 13], "harder": 9, "have": [4, 9, 13], "help": [9, 10, 13], "helvetica": [], "here": 13, "hint": 10, "how": 13, "howev": 13, "i": [0, 1, 2, 4, 7, 9, 10, 13], "id": 10, "idx": 13, "immedi": 9, "immut": [9, 11], "implement": [0, 11, 13], "impli": 13, "implicit": 13, "implicitli": 13, "import": [0, 9, 13], "importerror": [], "inadvert": [11, 13], "includ": [0, 4, 13], "incompat": 4, "incomplet": [], "incomplete_fillcolor": [], "incomplete_linecolor": [], "incorrect": 9, "independ": 0, "index": [4, 7], "indic": 9, "individu": [12, 13], "infer": 10, "inform": [2, 10], "inherit": [10, 11, 13], "initi": 9, "input": [10, 11, 13], "inspect": 9, "instal": [10, 11], "instead": 9, "int": [4, 9, 10, 13], "integr": 10, "interfac": 10, "interfer": 10, "intern": 13, "invalid": 13, "item": 7, "its": [0, 4, 10, 13], "j": 13, "keep": 13, "kei": [7, 9, 13], "kwarg": [2, 6], "languag": [9, 10], "laod": 13, "larg": 13, "layout": [], "lead": [9, 13], "legaci": 2, "len": 13, "let": [0, 9, 13], "level": [4, 13], "librari": 10, "lightblu": [], "lightweight": 10, "like": 13, "limit": [10, 13], "list": [2, 4, 6, 8, 13], "load": [2, 9, 10, 11], "load_bas": 0, "load_base_data": 0, "load_data": [0, 13], "load_mixin": 0, "load_port": [], "load_raw": [], "loaded_analysi": 13, "logic": 10, "look": [0, 13], "lr": [], "made": 10, "mai": 13, "maintain": [0, 10, 11, 13], "make": [9, 10, 13], "manag": [7, 11, 13], "manifest": 10, "manual": 10, "map": 4, "matter": 13, "maximum": 4, "mean": [4, 9, 13], "mechan": 9, "memori": 10, "messag": 10, "met": 13, "metadata": [2, 5, 7, 10, 11, 13], "metadata_report": 2, "method": [2, 6, 7, 9, 10, 13], "might": 13, "minimalist": 10, "mixin_data": 0, "mixinanalysi": 0, "modif": 10, "modifi": 7, "modul": 10, "modular": 0, "monitor": 11, "more": [2, 10, 12, 13], "multipl": [0, 10, 13], "must": [4, 9, 10], "mutabilityconflicterror": [4, 5, 13], "mutabl": 4, "mutat": [1, 4, 7, 8, 10, 11, 13], "myanalysi": 13, "name": [0, 4, 7, 8, 13], "nativ": 10, "natur": [0, 10], "navi": [], "need": 13, "nice": 9, "no_result": [2, 13], "node": 4, "none": [1, 2, 4, 7, 8], "note": 13, "notimplementederror": [], "object": [2, 6, 7, 10, 13], "offer": 11, "onc": [2, 10, 13], "one": 10, "ones": 0, "onli": [2, 4, 13], "oper": [10, 13], "option": [2, 7], "order": [2, 10, 13], "organ": 13, "origin": [0, 10, 11], "other": 10, "otherwis": 2, "out": [10, 13], "output": [10, 11, 13], "outsid": 7, "over": 10, "overlap": 13, "overrid": [], "overwrit": 2, "palegreen": [], "panic": 13, "panic_on_exist": [2, 13], "parallel": 10, "paramet": [2, 4, 7, 8, 10, 13], "pars": 1, "particularli": [], "pass": 2, "path": 2, "pattern": 10, "pdf": [], "perform": [1, 9], "persist": 11, "philosophi": 11, "pickl": [2, 10], "pip": 12, "pipelin": [0, 2, 10, 11], "pkl": 10, "place": 13, "plot": [], "plottingmixin": [], "point": 10, "portabl": 11, "potenti": [10, 13], "power": [0, 10], "practic": 10, "preserv": 10, "prevent": 10, "previou": 13, "primari": 9, "principl": 11, "print": [9, 13], "problem": 13, "proc_a": 0, "proc_b": 0, "proc_c": 0, "proc_x": 13, "proc_y1": 13, "proc_y2": 13, "proc_z": 13, "process": [0, 9], "process_a": 0, "process_al": 0, "process_b": 0, "process_c": 0, "process_data": [9, 10], "process_i": 13, "process_x": 13, "process_z": 13, "processed_data": [9, 10, 13], "progress": 11, "properli": 13, "properti": [2, 10], "protect": [10, 11], "proven": [11, 13], "provid": [2, 9, 10, 11, 13], "pure": [10, 11], "purpos": 10, "python": [0, 10, 11, 12, 13], "quick": 11, "rais": [1, 2, 7, 9, 13], "rang": [0, 13], "rankdir": [], "rather": [9, 10], "raw_data": [9, 10, 13], "rawanalysi": [], "read": 4, "read_graph": 4, "reason": [9, 10, 13], "reassign": 13, "record": 13, "refer": 11, "reflect": 13, "regist": 8, "regular": 4, "reinforc": 13, "relat": 10, "relationship": 10, "reload": 10, "remain": 10, "rememb": [], "render": 2, "replac": [], "report": 2, "reproduc": [10, 11, 13], "requir": [0, 1, 6, 8, 9, 10, 13], "requires_flag": 8, "rerun": 13, "result": [0, 2, 5, 8, 9, 11, 13], "resultslock": [5, 7], "return": [0, 1, 2, 4, 7, 8, 9, 10, 13], "reusabl": 0, "rich": 12, "run": [0, 2, 9, 10, 13], "runnabl": 13, "same": [0, 4, 13], "save": [2, 11], "seamlessli": 0, "second": 13, "secur": 10, "see": [10, 13], "select": [2, 10], "self": [0, 1, 9, 10, 13], "separ": 10, "serial": 11, "serv": 10, "set": [4, 7], "set_metadata": 7, "sever": 10, "share": [0, 4, 11, 13], "shareabl": 10, "should": [10, 13], "show": [0, 13], "side": [9, 13], "signifi": 13, "significantli": 13, "similar": 9, "simpl": [0, 11], "simpleanalysi": 0, "simpler": 0, "simplic": 10, "singl": 10, "size": [], "skip": [2, 13], "so": [10, 13], "solut": [11, 13], "some": [10, 13], "some_result_nam": 10, "sometim": 13, "sourc": [1, 2, 4, 6, 7, 8, 9], "specif": [2, 7, 10, 12, 13], "specifi": 13, "standard": [0, 10], "start": 11, "state": [9, 10, 11], "static": 9, "step": [2, 4, 5, 6, 7, 9, 11], "step_a": [], "step_b": [], "step_c": [], "step_fillcolor": [], "step_linecolor": [], "step_metadata": [], "step_nam": [2, 7], "still": [10, 13], "stop": 9, "storag": 10, "store": [10, 13], "str": [2, 4, 6, 7, 8], "strongli": 10, "structur": [9, 10, 11, 13], "stub": [], "style": 10, "subclass": [], "subset": [12, 13], "suit": [], "sum": 13, "super": 0, "support": 10, "syntax": [5, 10, 11, 13], "t": 10, "take": 13, "tar": 10, "target_step": [2, 13], "templat": 0, "templateanalysi": [], "text": [], "than": [2, 9, 10], "thei": [0, 2], "them": 13, "theres": 13, "thi": [0, 2, 8, 9, 10, 13], "thing": 13, "third": 13, "thread": 7, "threadsafelock": [], "three": 13, "through": [10, 11], "time": [2, 9, 10, 13], "timestamp": 6, "to_dict": 6, "toml": 10, "tool": 10, "topolog": [4, 13], "track": [0, 9, 10, 11], "tradeoff": 11, "transform": [11, 13], "travers": 10, "tree": [5, 11], "true": [10, 13], "try": [9, 13], "tupl": 13, "type": [1, 2, 4, 7, 8, 9, 10], "unauthorizedmutationerror": [5, 7], "undeclar": [1, 9], "underscor": 13, "understand": 13, "unexpect": 9, "unpack": 10, "unpickl": 10, "untrust": 10, "up": [2, 13], "updat": 13, "upfront": 10, "us": [0, 1, 2, 9, 10, 12, 13], "usag": [10, 11], "user": [10, 13], "valid": [1, 4, 10, 11], "validate_ast": [1, 5], "validate_incompatible_mut": [4, 5], "valu": 4, "valueerror": 2, "variabl": [1, 9, 13], "ve": 13, "veri": 13, "verifi": 9, "version": 10, "view": 13, "visual": [2, 10, 11], "visualize_depend": [0, 2, 13], "viz": 12, "wa": 10, "wai": 13, "want": [12, 13], "we": [9, 13], "well": [10, 13], "were": 2, "what": [10, 13], "when": [0, 1, 7, 9, 10, 13], "where": [11, 13], "whether": 2, "which": [2, 9, 10, 13], "while": [0, 10], "white": [], "within": 13, "without": [9, 10, 11], "work": [0, 10, 13], "workflow": [9, 10, 11, 13], "workflow_step_a": 13, "workflow_step_b": 13, "workflow_step_c": 13, "workflow_step_d": 13, "would": 9, "wrap": 9, "write": 4, "write_graph": 4, "x": 13, "y": 13, "yaflux": [0, 1, 2, 4, 6, 7, 8, 9, 10, 12, 13], "yax": [2, 10, 13], "yf": [0, 9, 10, 13], "you": [0, 9, 12, 13], "your": [0, 13], "z": 13, "zero": [10, 12], "zip": 0}, "titles": ["Advanced Usage", "Abstract Syntax Tree", "Base Class", "Executor", "Graph", "API Reference", "Metadata", "Results", "Step Decorator", "Abstract Syntax Tree (AST)", "Design Philosophy", "yaflux", "Installation", "Quick Start"], "titleterms": {"1": 10, "2": 10, "3": 10, "4": 10, "5": 10, "abstract": [1, 9], "access": 0, "advanc": 0, "an": 13, "analysi": [0, 10, 13], "api": [5, 11], "approach": 10, "assign": 9, "ast": 9, "base": [2, 10], "basic": 0, "best": 0, "class": [2, 10, 13], "common": [], "consider": 10, "content": 11, "core": 10, "custom": 10, "decis": 10, "decor": [8, 10, 13], "defin": 13, "definit": [10, 13], "depend": [0, 9, 10, 13], "design": 10, "direct": 9, "exampl": 13, "execut": 13, "executor": 3, "explicit": 10, "explicitli": 10, "fail": 10, "fast": 10, "featur": [0, 11], "flag": 13, "function": 10, "futur": 10, "graph": 4, "immut": 10, "implement": 10, "implicit": 10, "infer": 13, "infrastructur": 10, "inherit": 0, "instal": 12, "kei": 11, "level": 0, "load": 13, "manag": 10, "metadata": 6, "method": 0, "minim": 10, "mixin": [], "multi": 0, "mutabl": 13, "origin": 13, "overrid": 0, "overview": 11, "parent": 0, "pattern": [], "philosophi": 10, "portabl": 10, "practic": 0, "principl": 10, "progress": [], "quick": 13, "redund": 13, "refer": 5, "refin": [], "result": [7, 10], "runtim": 13, "save": 13, "select": 13, "serial": 10, "set": 13, "start": 13, "state": 13, "step": [0, 8, 10, 13], "support": 0, "syntax": [1, 9], "templat": [], "track": 13, "tradeoff": 10, "tree": [1, 9], "usag": [0, 9], "v": 10, "valid": 9, "visual": [0, 13], "without": 13, "yaflux": 11}})