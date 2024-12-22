#include <kdl/kdl.h>

#include "test_util.h"

#include <math.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

static void test_basics_v1(void)
{
    kdl_emitter_options emitter_opt = KDL_DEFAULT_EMITTER_OPTIONS;
    emitter_opt.version = KDL_VERSION_1;
    emitter_opt.indent = 3;
    emitter_opt.float_mode.always_write_decimal_point_or_exponent = false;
    kdl_emitter* emitter = kdl_create_buffering_emitter(&emitter_opt);

    char const* expected = "\xf0\x9f\x92\xa9\n"
                           "node2 {\n"
                           "   \"first child\" 1 a=\"b\"\n"
                           "   (ta)second-child\n"
                           "}\n"
                           "node3\n";
    kdl_str expected_str = kdl_str_from_cstr(expected);

    ASSERT(kdl_emit_node(emitter, kdl_str_from_cstr("\xf0\x9f\x92\xa9")));
    ASSERT(kdl_emit_node(emitter, kdl_str_from_cstr("node2")));
    ASSERT(kdl_start_emitting_children(emitter));
    ASSERT(kdl_emit_node(emitter, kdl_str_from_cstr("first child")));
    kdl_value v;
    v.type = KDL_TYPE_NUMBER;
    v.type_annotation = (kdl_str){NULL, 0};
    v.number = (kdl_number){.type = KDL_NUMBER_TYPE_FLOATING_POINT, .floating_point = 1.0};
    ASSERT(kdl_emit_arg(emitter, &v));
    v.type = KDL_TYPE_STRING;
    v.string = kdl_str_from_cstr("b");
    ASSERT(kdl_emit_property(emitter, kdl_str_from_cstr("a"), &v));
    ASSERT(kdl_emit_node_with_type(emitter, kdl_str_from_cstr("ta"), kdl_str_from_cstr("second-child")));
    ASSERT(kdl_finish_emitting_children(emitter));
    ASSERT(kdl_emit_node(emitter, kdl_str_from_cstr("node3")));
    ASSERT(kdl_emit_end(emitter));

    kdl_str result = kdl_get_emitter_buffer(emitter);
    ASSERT(result.len == expected_str.len);
    ASSERT(memcmp(result.data, expected_str.data, result.len) == 0);

    kdl_destroy_emitter(emitter);
}

static void test_basics_v2(void)
{
    kdl_emitter_options emitter_opt = KDL_DEFAULT_EMITTER_OPTIONS;
    emitter_opt.indent = 3;
    emitter_opt.float_mode.always_write_decimal_point_or_exponent = false;
    kdl_emitter* emitter = kdl_create_buffering_emitter(&emitter_opt);

    char const* expected = "\xf0\x9f\x92\xa9\n"
                           "node2 {\n"
                           "   \"first child\" 1 a=b\n"
                           "   (ta)second-child\n"
                           "}\n"
                           "node3\n";
    kdl_str expected_str = kdl_str_from_cstr(expected);

    ASSERT(kdl_emit_node(emitter, kdl_str_from_cstr("\xf0\x9f\x92\xa9")));
    ASSERT(kdl_emit_node(emitter, kdl_str_from_cstr("node2")));
    ASSERT(kdl_start_emitting_children(emitter));
    ASSERT(kdl_emit_node(emitter, kdl_str_from_cstr("first child")));
    kdl_value v;
    v.type = KDL_TYPE_NUMBER;
    v.type_annotation = (kdl_str){NULL, 0};
    v.number = (kdl_number){.type = KDL_NUMBER_TYPE_FLOATING_POINT, .floating_point = 1.0};
    ASSERT(kdl_emit_arg(emitter, &v));
    v.type = KDL_TYPE_STRING;
    v.string = kdl_str_from_cstr("b");
    ASSERT(kdl_emit_property(emitter, kdl_str_from_cstr("a"), &v));
    ASSERT(kdl_emit_node_with_type(emitter, kdl_str_from_cstr("ta"), kdl_str_from_cstr("second-child")));
    ASSERT(kdl_finish_emitting_children(emitter));
    ASSERT(kdl_emit_node(emitter, kdl_str_from_cstr("node3")));
    ASSERT(kdl_emit_end(emitter));

    kdl_str result = kdl_get_emitter_buffer(emitter);
    ASSERT(result.len == expected_str.len);
    ASSERT(memcmp(result.data, expected_str.data, result.len) == 0);

    kdl_destroy_emitter(emitter);
}

static void test_data_types(void)
{
    kdl_emitter* emitter = kdl_create_buffering_emitter(&KDL_DEFAULT_EMITTER_OPTIONS);

    ASSERT(emitter);
    ASSERT(kdl_emit_node(emitter, kdl_str_from_cstr("-")));

    ASSERT(kdl_emit_arg(emitter,
        &(kdl_value){
            .type = KDL_TYPE_NUMBER,
            .number = (kdl_number){.type = KDL_NUMBER_TYPE_INTEGER, .integer = -100}
    }));
    ASSERT(kdl_emit_arg(emitter,
        &(kdl_value){
            .type = KDL_TYPE_NUMBER,
            .number = (kdl_number){.type = KDL_NUMBER_TYPE_FLOATING_POINT, .floating_point = -INFINITY}
    }));
    ASSERT(kdl_emit_arg(emitter, &(kdl_value){.type = KDL_TYPE_STRING, .string = kdl_str_from_cstr("abc")}));
    ASSERT(
        kdl_emit_arg(emitter, &(kdl_value){.type = KDL_TYPE_STRING, .string = kdl_str_from_cstr("abc def")}));
    ASSERT(kdl_emit_arg(emitter, &(kdl_value){.type = KDL_TYPE_BOOLEAN, .boolean = true}));
    ASSERT(kdl_emit_arg(emitter, &(kdl_value){.type = KDL_TYPE_BOOLEAN, .boolean = false}));
    ASSERT(kdl_emit_arg(emitter, &(kdl_value){.type = KDL_TYPE_NULL}));
    ASSERT(kdl_emit_end(emitter));

    kdl_str result = kdl_get_emitter_buffer(emitter);

    char const* expected = "- -100 #-inf abc \"abc def\" #true #false #null\n";
    kdl_str expected_str = kdl_str_from_cstr(expected);
    ASSERT(expected_str.len == result.len);
    ASSERT(memcmp(result.data, expected_str.data, result.len) == 0);
}

static void test_ascii_mode(void)
{
    kdl_emitter_options opts = KDL_DEFAULT_EMITTER_OPTIONS;
    opts.escape_mode = KDL_ESCAPE_ASCII_MODE;
    kdl_emitter* emitter = kdl_create_buffering_emitter(&opts);

    ASSERT(emitter);
    ASSERT(kdl_emit_node(emitter, kdl_str_from_cstr("\xc3\xa4"))); // ä U+00E4
    ASSERT(kdl_emit_arg(
        emitter, &(kdl_value){.type = KDL_TYPE_STRING, .string = kdl_str_from_cstr("\xc3\xb6")})); // ö U+00F6
    ASSERT(kdl_emit_end(emitter));

    kdl_str result = kdl_get_emitter_buffer(emitter);

    char const* expected = "\"\\u{e4}\" \"\\u{f6}\"\n";
    kdl_str expected_str = kdl_str_from_cstr(expected);

    ASSERT(expected_str.len == result.len);
    ASSERT(memcmp(result.data, expected_str.data, result.len) == 0);
}

void TEST_MAIN(void)
{
    run_test("Emitter: basics (v1)", &test_basics_v1);
    run_test("Emitter: basics (v2)", &test_basics_v2);
    run_test("Emitter: all types", &test_data_types);
    run_test("Emitter: ASCII mode", &test_ascii_mode);
}
