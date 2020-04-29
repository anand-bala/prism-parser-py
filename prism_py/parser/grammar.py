from arpeggio import *
from arpeggio import RegExMatch as _


# fmt: off
def comment(): return _(r"//.*$")
def skip(): return ZeroOrMore([DEFAULT_WS, comment])
# fmt: on

##############
#  Keywords  #
##############


class Keywd(StrMatch):
    _keyword_table = []

    def __init__(self, to_match):
        super(Keywd, self).__init__(to_match)
        self.to_match = to_match
        self.root = True
        self.rule_name = "keyword"


# fmt: off
def kw_bool(): return Keywd("bool")
def kw_clock(): return Keywd("clock")
def kw_const(): return Keywd("const")
def kw_ctmc(): return Keywd("ctmc")
def kw_double(): return Keywd("double")
def kw_dtmc(): return Keywd("dtmc")
def kw_endinit(): return Keywd("endinit")
def kw_endinvariant(): return Keywd("endinvariant")
def kw_endmodule(): return Keywd("endmodule")
def kw_endrewards(): return Keywd("endrewards")
def kw_endsystem(): return Keywd("endsystem")
def kw_false(): return Keywd("false")
def kw_filter(): return Keywd("filter")
def kw_formula(): return Keywd("formula")
def kw_func(): return Keywd("func")
def kw_global(): return Keywd("global")
def kw_init(): return Keywd("init")
def kw_int(): return Keywd("int")
def kw_invariant(): return Keywd("invariant")
def kw_label(): return Keywd("label")
def kw_max(): return Keywd("max")
def kw_mdp(): return Keywd("mdp")
def kw_min(): return Keywd("min")
def kw_module(): return Keywd("module")
def kw_nondeterministic(): return Keywd("nondeterministic")
def kw_prob(): return Keywd("prob")
def kw_probabilistic(): return Keywd("probabilistic")
def kw_pta(): return Keywd("pta")
def kw_rate(): return Keywd("rate")
def kw_rewards(): return Keywd("rewards")
def kw_stochastic(): return Keywd("stochastic")
def kw_system(): return Keywd("system")
def kw_true(): return Keywd("true")
# fmt: on


def reserved_keywords():
    return _(
        r"({})\b".format(
            "|".join(
                [
                    "bool",
                    "clock",
                    "const",
                    "ctmc",
                    "double",
                    "dtmc",
                    "endinit",
                    "endinvariant",
                    "endmodule",
                    "endrewards",
                    "endsystem",
                    "false",
                    "filter",
                    "formula",
                    "func",
                    "global",
                    "init",
                    "int",
                    "invariant",
                    "label",
                    "max",
                    "mdp",
                    "min",
                    "module",
                    "nondeterministic",
                    "prob",
                    "probabilistic",
                    "pta",
                    "rate",
                    "rewards",
                    "stochastic",
                    "system",
                    "true",
                ]
            )
        )
    )


####################
#  Basic Literals  #
####################


###############
#  Primitives #
###############

# fmt: off
def boolean(): return [kw_true, kw_false]
def integer(): return _(r"\d+")
def double(): return _(r"\d*\.\d+([Ee][+-]?\d+)?")
def number(): return [ double, integer ]
def ident(): return Not(reserved_keywords), _(r"[A-Za-z_][A-Za-z0-9_]*")
# fmt: on

#######################
#  Builtin Functions  #
#######################


class Builtin(StrMatch):
    _builtin_table = []

    def __init__(self, to_match):
        super(Builtin, self).__init__(to_match)
        self.to_match = to_match
        self.root = True
        self.rule_name = "builtin"
        if to_match not in Builtin._builtin_table:
            Builtin._builtin_table.append(to_match)


# fmt: off
def builtin_min(): return Builtin("min")
def builtin_max(): return Builtin("max")
def builtin_floor(): return Builtin("floor")
def builtin_ceil(): return Builtin("ceil")
def builtin_round(): return Builtin("round")
def builtin_pow(): return Builtin("pow")
def builtin_mod(): return Builtin("mod")
def builtin_log(): return Builtin("log")
# fmt: on


def builtins():
    return _(
        r"(({}))".format(
            "|".join(["min", "max", "floor", "ceil", "round", "pow", "mod", "log"])
        )
    )


###############
#  Operators  #
###############


def unary_op():
    return [lnot_op, add_op]


# fmt: off
def mul_op(): return [ "*", "/" ]
def add_op(): return [ "+", "-" ]
def relational_op(): return [ "<=", ">=", "<", ">" ]
def equality_op(): return [ "!=", "=" ]
def lnot_op(): return "!"
def land_op(): return "&"
def lor_op(): return "|"
def liff_op(): return "<=>"
def limp_op(): return "=>"
# fmt: on

#################
#  Expressions  #
#################
# An expression can consist of literals (numbers), identifiers, and operations
# on them (arithmetic, boolean, comparison, conditionals, and functions)

# TODO: Left-associative rules can be fixed in post. Essentially all OneOrMore rules...

# fmt: off
def ArgumentExprList(): return ZeroOrMore(Expression, sep=",")
def FunctionCall(): return builtins, "(", ArgumentExprList, ")"

def ParenExpr(): return "(", Expression, ")"

def TermExpr(): return [number, ident, FunctionCall ]
def PrefixExpr(): return [(Optional(unary_op), TermExpr), ParenExpr]
def MultiplyExpr(): return OneOrMore(PrefixExpr, sep=mul_op)
def AdditionExpr(): return OneOrMore(MultiplyExpr, sep=add_op)
def CompareExpr(): return OneOrMore(AdditionExpr, sep=relational_op)
def EqualityExpr(): return OneOrMore(CompareExpr, sep=equality_op)
def LogicalAndExpr(): return OneOrMore(EqualityExpr, sep=land_op)
def LogicalOrExpr(): return OneOrMore(LogicalAndExpr, sep=lor_op)
def LogicalIffExpr(): return OneOrMore(LogicalOrExpr, sep=liff_op)
def LogicalImplExpr(): return OneOrMore(LogicalIffExpr, sep=limp_op)
def ConditionalExpr(): return LogicalImplExpr, Optional("?", Expression, ":", Expression)
def Expression(): return ConditionalExpr
def ConstExpression(): return Expression


# fmt: on

######################
#  Type Declaration  #
######################

# fmt: off

def Decl_Type(): return [kw_int, kw_clock, kw_bool]
def Decl_ConstType(): return [kw_int, kw_bool, kw_double, kw_prob, kw_rate]

# fmt: on

##################
#  Reward Block  #
##################

# fmt: off

def Reward_Guard(): return Expression
def Reward_Action(): return Command_Action
def Reward_Item(): return Optional(Reward_Action), Reward_Guard, ":", Expression, ";"

# fmt: on

########################
#  Module Declaration  #
########################

# fmt: off

def Decl_Invariants(): return kw_invariant, Expression, kw_endinvariant

def Var_Init(): return kw_init, ConstExpression
def Var_Range(): return "[", ConstExpression, "..", ConstExpression, "]"
def Decl_Var(): return ident, ":", [Var_Range, Decl_Type] , Optional(Var_Init), ";"

def ProbabilityExpr(): return ConstExpression
def UpdateVarExpr(): return ident, "'", "=", ConstExpression
def UpdateExpr(): return OneOrMore(Optional(ProbabilityExpr, ":"), OneOrMore("(",UpdateVarExpr, ")", sep="&"), sep="+")
def Command_Update(): return [ kw_true, UpdateExpr ]

def Command_Action(): return "[", Optional(ident), "]"
def Command_Guard(): return Expression
def Decl_Command(): return Command_Action, Command_Guard, "->", Command_Update, ";"

def Module_Content(): return ZeroOrMore([Decl_Var, Decl_Command, Decl_Invariants ])

def Rename_Term(): return [builtins, ident], "=", [builtins, ident]
def Rename_List(): return "[", ZeroOrMore(Rename_Term, sep=",") ,"]"
def Module_Rename(): return "=", ident, Rename_List
# fmt: on

#####################
#  Top-level stuff  #
#####################


def Decl_Reward():
    return kw_rewards, '"', ident, '"', ZeroOrMore(Reward_Item), kw_endrewards


def Decl_Label():
    return kw_label, '"', ident, '"', "=", Expression, ";"


def Decl_Formula():
    return kw_formula, ident, "=", Expression, ";"


def Decl_GlobalVar():
    return kw_global, Decl_Var


def Decl_InitBlock():
    return kw_init, Expression, kw_endinit


# TODO: Module Renaming
def Decl_Module():
    return kw_module, ident, [Module_Rename, Module_Content], kw_endmodule


# TODO: Undefined Const
def Decl_Const():
    return kw_const, Decl_ConstType, ident, "=", ConstExpression, ";"


def Decl_ModelType():
    return [kw_mdp, kw_ctmc, kw_dtmc, kw_pta]


def TopLevel():
    return [
        Decl_Module,
        Decl_Const,
        Decl_ModelType,
        Decl_InitBlock,
        Decl_GlobalVar,
        Decl_Formula,
        Decl_Label,
    ]


def ModelRoot():
    return OneOrMore(TopLevel), EOF
