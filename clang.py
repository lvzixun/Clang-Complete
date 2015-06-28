# the type from clang-c/Index.h

from ctypes import Structure, POINTER, c_char_p, c_void_p, c_uint, c_bool, c_ulong, c_int
from .enum import Enum

class CXUnsavedFile(Structure):
  _fields_ = [("name", c_char_p), ("contents", c_char_p), ('length', c_ulong)]


class CXCompletionChunkKind(Enum):
  Optional = 0
  TypedText = 1
  Text = 2
  Placeholder = 3
  Informative = 4
  CurrentParameter = 5
  LeftParen = 6
  RightParen = 7
  LeftBracket = 8
  RightBracket = 9
  LeftBrace = 10
  RightBrace = 11
  LeftAngle = 12
  RightAngle = 13
  Comma = 14
  ResultType = 15
  Colon = 16
  SemiColon = 17
  Equal = 18
  HorizontalSpace = 19
  VerticalSpace = 20


class CXCursorKind(Enum):
  UNEXPOSED_DECL =  1 

  # A C or C++ struct.
  STRUCT_DECL =  2 

  # A C or C++ union.
  UNION_DECL =  3 

  # A C++ class.
  CLASS_DECL =  4 

  # An enumeration.
  ENUM_DECL =  5 

  # A field (in C  or non-static data member (in C++  in a struct, union, or C++
  # class.
  FIELD_DECL =  6 

  # An enumerator constant.
  ENUM_CONSTANT_DECL =  7 

  # A function.
  FUNCTION_DECL =  8 

  # A variable.
  VAR_DECL =  9 

  # A function or method parameter.
  PARM_DECL =  10 

  # An Objective-C @interface.
  OBJC_INTERFACE_DECL =  11 

  # An Objective-C @interface for a category.
  OBJC_CATEGORY_DECL =  12 

  # An Objective-C @protocol declaration.
  OBJC_PROTOCOL_DECL =  13 

  # An Objective-C @property declaration.
  OBJC_PROPERTY_DECL =  14 

  # An Objective-C instance variable.
  OBJC_IVAR_DECL =  15 

  # An Objective-C instance method.
  OBJC_INSTANCE_METHOD_DECL =  16 

  # An Objective-C class method.
  OBJC_CLASS_METHOD_DECL =  17 

  # An Objective-C @implementation.
  OBJC_IMPLEMENTATION_DECL =  18 

  # An Objective-C @implementation for a category.
  OBJC_CATEGORY_IMPL_DECL =  19 

  # A typedef.
  TYPEDEF_DECL =  20 

  # A C++ class method.
  CXX_METHOD =  21 

  # A C++ namespace.
  NAMESPACE =  22 

  # A linkage specification, e.g. 'extern "C"'.
  LINKAGE_SPEC =  23 

  # A C++ constructor.
  CONSTRUCTOR =  24 

  # A C++ destructor.
  DESTRUCTOR =  25 

  # A C++ conversion function.
  CONVERSION_FUNCTION =  26 

  # A C++ template type parameter
  TEMPLATE_TYPE_PARAMETER =  27 

  # A C++ non-type template paramater.
  TEMPLATE_NON_TYPE_PARAMETER =  28 

  # A C++ template template parameter.
  TEMPLATE_TEMPLATE_PARAMTER =  29 

  # A C++ function template.
  FUNCTION_TEMPLATE =  30 

  # A C++ class template.
  CLASS_TEMPLATE =  31 

  # A C++ class template partial specialization.
  CLASS_TEMPLATE_PARTIAL_SPECIALIZATION =  32 

  # A C++ namespace alias declaration.
  NAMESPACE_ALIAS =  33 

  # A C++ using directive
  USING_DIRECTIVE =  34 

  # A C++ using declaration
  USING_DECLARATION =  35 

  # A Type alias decl.
  TYPE_ALIAS_DECL =  36 

  # A Objective-C synthesize decl
  OBJC_SYNTHESIZE_DECL =  37 

  # A Objective-C dynamic decl
  OBJC_DYNAMIC_DECL =  38 

  # A C++ access specifier decl.
  CXX_ACCESS_SPEC_DECL =  39 


  ###
  # Reference Kinds

  OBJC_SUPER_CLASS_REF =  40 
  OBJC_PROTOCOL_REF =  41 
  OBJC_CLASS_REF =  42 

  # A reference to a type declaration.
  #
  # A type reference occurs anywhere where a type is named but not
  # declared. For example, given:
  #   typedef unsigned size_type;
  #   size_type size;
  #
  # The typedef is a declaration of size_type (CXCursor_TypedefDecl ,
  # while the type of the variable "size" is referenced. The cursor
  # referenced by the type of size is the typedef for size_type.
  TYPE_REF =  43 
  CXX_BASE_SPECIFIER =  44 

  # A reference to a class template, function template, template
  # template parameter, or class template partial specialization.
  TEMPLATE_REF =  45 

  # A reference to a namespace or namepsace alias.
  NAMESPACE_REF =  46 

  # A reference to a member of a struct, union, or class that occurs in
  # some non-expression context, e.g., a designated initializer.
  MEMBER_REF =  47 

  # A reference to a labeled statement.
  LABEL_REF =  48 

  # A reference toa a set of overloaded functions or function templates
  # that has not yet been resolved to a specific function or function template.
  OVERLOADED_DECL_REF =  49 

  ###
  # Invalid/Error Kinds

  INVALID_FILE =  70 
  NO_DECL_FOUND =  71 
  NOT_IMPLEMENTED =  72 
  INVALID_CODE =  73 

  ###
  # Expression Kinds

  # An expression whose specific kind is not exposed via this interface.
  #
  # Unexposed expressions have the same operations as any other kind of
  # expression; one can extract their location information, spelling, children,
  # etc. However, the specific kind of the expression is not reported.
  UNEXPOSED_EXPR =  100 

  # An expression that refers to some value declaration, such as a function,
  # varible, or enumerator.
  DECL_REF_EXPR =  101 

  # An expression that refers to a member of a struct, union, class, Objective-C
  # class, etc.
  MEMBER_REF_EXPR =  102 

  # An expression that calls a function.
  CALL_EXPR =  103 

  # An expression that sends a message to an Objective-C object or class.
  OBJC_MESSAGE_EXPR =  104 

  # An expression that represents a block literal.
  BLOCK_EXPR =  105 

  # An integer literal.
  INTEGER_LITERAL =  106 

  # A floating point number literal.
  FLOATING_LITERAL =  107 

  # An imaginary number literal.
  IMAGINARY_LITERAL =  108 

  # A string literal.
  STRING_LITERAL =  109 

  # A character literal.
  CHARACTER_LITERAL =  110 

  # A parenthesized expression, e.g. "(1 ".
  #
  # This AST node is only formed if full location information is requested.
  PAREN_EXPR =  111 

  # This represents the unary-expression's (except sizeof and
  # alignof .
  UNARY_OPERATOR =  112 

  # [C99 6.5.2.1] Array Subscripting.
  ARRAY_SUBSCRIPT_EXPR =  113 

  # A builtin binary operation expression such as "x + y" or
  # "x <= y".
  BINARY_OPERATOR =  114 

  # Compound assignment such as "+=".
  COMPOUND_ASSIGNMENT_OPERATOR =  115 

  # The ?: ternary operator.
  CONDITONAL_OPERATOR =  116 

  # An explicit cast in C (C99 6.5.4  or a C-style cast in C++
  # (C++ [expr.cast] , which uses the syntax (Type expr.
  #
  # For example: (int f.
  CSTYLE_CAST_EXPR =  117 

  # [C99 6.5.2.5]
  COMPOUND_LITERAL_EXPR =  118 

  # Describes an C or C++ initializer list.
  INIT_LIST_EXPR =  119 

  # The GNU address of label extension, representing &&label.
  ADDR_LABEL_EXPR =  120 

  # This is the GNU Statement Expression extension: ({int X=4; X;} 
  StmtExpr =  121 

  # Represents a C1X generic selection.
  GENERIC_SELECTION_EXPR =  122 

  # Implements the GNU __null extension, which is a name for a null
  # pointer constant that has integral type (e.g., int or long  and is the same
  # size and alignment as a pointer.
  #
  # The __null extension is typically only used by system headers, which define
  # NULL as __null in C++ rather than using 0 (which is an integer that may not
  # match the size of a pointer .
  GNU_NULL_EXPR =  123 

  # C++'s static_cast<> expression.
  CXX_STATIC_CAST_EXPR =  124 

  # C++'s dynamic_cast<> expression.
  CXX_DYNAMIC_CAST_EXPR =  125 

  # C++'s reinterpret_cast<> expression.
  CXX_REINTERPRET_CAST_EXPR =  126 

  # C++'s const_cast<> expression.
  CXX_CONST_CAST_EXPR =  127 

  # Represents an explicit C++ type conversion that uses "functional"
  # notion (C++ [expr.type.conv] .
  #
  # Example:
  # \code
  #   x = int(0.5 ;
  # \endcode
  CXX_FUNCTIONAL_CAST_EXPR =  128 

  # A C++ typeid expression (C++ [expr.typeid] .
  CXX_TYPEID_EXPR =  129 

  # [C++ 2.13.5] C++ Boolean Literal.
  CXX_BOOL_LITERAL_EXPR =  130 

  # [C++0x 2.14.7] C++ Pointer Literal.
  CXX_NULL_PTR_LITERAL_EXPR =  131 

  # Represents the "this" expression in C++
  CXX_THIS_EXPR =  132 

  # [C++ 15] C++ Throw Expression.
  #
  # This handles 'throw' and 'throw' assignment-expression. When
  # assignment-expression isn't present, Op will be null.
  CXX_THROW_EXPR =  133 

  # A new expression for memory allocation and constructor calls, e.g:
  # "new CXXNewExpr(foo ".
  CXX_NEW_EXPR =  134 

  # A delete expression for memory deallocation and destructor calls,
  # e.g. "delete[] pArray".
  CXX_DELETE_EXPR =  135 

  # Represents a unary expression.
  CXX_UNARY_EXPR =  136 

  # ObjCStringLiteral, used for Objective-C string literals i.e. "foo".
  OBJC_STRING_LITERAL =  137 

  # ObjCEncodeExpr, used for in Objective-C.
  OBJC_ENCODE_EXPR =  138 

  # ObjCSelectorExpr used for in Objective-C.
  OBJC_SELECTOR_EXPR =  139 

  # Objective-C's protocol expression.
  OBJC_PROTOCOL_EXPR =  140 

  # An Objective-C "bridged" cast expression, which casts between
  # Objective-C pointers and C pointers, transferring ownership in the process.
  #
  # \code
  #   NSString *str = (__bridge_transfer NSString * CFCreateString( ;
  # \endcode
  OBJC_BRIDGE_CAST_EXPR =  141 

  # Represents a C++0x pack expansion that produces a sequence of
  # expressions.
  #
  # A pack expansion expression contains a pattern (which itself is an
  # expression  followed by an ellipsis. For example:
  PACK_EXPANSION_EXPR =  142 

  # Represents an expression that computes the length of a parameter
  # pack.
  SIZE_OF_PACK_EXPR =  143 

  # A statement whose specific kind is not exposed via this interface.
  #
  # Unexposed statements have the same operations as any other kind of statement;
  # one can extract their location information, spelling, children, etc. However,
  # the specific kind of the statement is not reported.
  UNEXPOSED_STMT =  200 

  # A labelled statement in a function.
  LABEL_STMT =  201 

  # A compound statement
  COMPOUND_STMT =  202 

  # A case statement.
  CASE_STMT =  203 

  # A default statement.
  DEFAULT_STMT =  204 

  # An if statement.
  IF_STMT =  205 

  # A switch statement.
  SWITCH_STMT =  206 

  # A while statement.
  WHILE_STMT =  207 

  # A do statement.
  DO_STMT =  208 

  # A for statement.
  FOR_STMT =  209 

  # A goto statement.
  GOTO_STMT =  210 

  # An indirect goto statement.
  INDIRECT_GOTO_STMT =  211 

  # A continue statement.
  CONTINUE_STMT =  212 

  # A break statement.
  BREAK_STMT =  213 

  # A return statement.
  RETURN_STMT =  214 

  # A GNU-style inline assembler statement.
  ASM_STMT =  215 

  # Objective-C's overall @try-@catch-@finally statement.
  OBJC_AT_TRY_STMT =  216 

  # Objective-C's @catch statement.
  OBJC_AT_CATCH_STMT =  217 

  # Objective-C's @finally statement.
  OBJC_AT_FINALLY_STMT =  218 

  # Objective-C's @throw statement.
  OBJC_AT_THROW_STMT =  219 

  # Objective-C's @synchronized statement.
  OBJC_AT_SYNCHRONIZED_STMT =  220 

  # Objective-C's autorealease pool statement.
  OBJC_AUTORELEASE_POOL_STMT =  221 

  # Objective-C's for collection statement.
  OBJC_FOR_COLLECTION_STMT =  222 

  # C++'s catch statement.
  CXX_CATCH_STMT =  223 

  # C++'s try statement.
  CXX_TRY_STMT =  224 

  # C++'s for (* : *  statement.
  CXX_FOR_RANGE_STMT =  225 

  # Windows Structured Exception Handling's try statement.
  SEH_TRY_STMT =  226 

  # Windows Structured Exception Handling's except statement.
  SEH_EXCEPT_STMT =  227 

  # Windows Structured Exception Handling's finally statement.
  SEH_FINALLY_STMT =  228 

  # The null statement.
  NULL_STMT =  230 

  # Adaptor class for mixing declarations with statements and expressions.
  DECL_STMT =  231 

  ###
  # Other Kinds

  # Cursor that represents the translation unit itself.
  #
  # The translation unit cursor exists primarily to act as the root cursor for
  # traversing the contents of a translation unit.
  TRANSLATION_UNIT =  300 

  ###
  # Attributes

  # An attribute whoe specific kind is note exposed via this interface
  UNEXPOSED_ATTR =  400 

  IB_ACTION_ATTR =  401 
  IB_OUTLET_ATTR =  402 
  IB_OUTLET_COLLECTION_ATTR =  403 

  ###
  # Preprocessing
  PREPROCESSING_DIRECTIVE =  500 
  MACRO_DEFINITION =  501 
  MACRO_INSTANTIATION =  502 
  INCLUSION_DIRECTIVE =  503 


# __all__ = ["CXUnsavedFile", "CXCompletionChunkKind", "CXCursorKind"]

