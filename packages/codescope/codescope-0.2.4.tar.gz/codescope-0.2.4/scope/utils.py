# Standard library
import os
import uuid
import shutil
from typing import List
import hashlib
import json

# Third party
from multilspy import SyncLanguageServer
from multilspy.multilspy_config import MultilspyConfig
from multilspy.multilspy_logger import MultilspyLogger

# Local
from scope.resources import EXT_TO_LANGUAGE_DATA
from scope.constants import (
    LANGUAGE_TO_LSP_LANGUAGE_MAP,
    TMP_DIR_PARENT,
)
from scope.dtos import Definition, Range

# Multispy currently supports "python", "rust", "csharp", "java"
# Need to support "JS/TS" and "Go"


def is_file_empty(path):
    return os.stat(path).st_size == 0


def root_contains_path(root_path, path):
    """
    1. Check if definition is outside of the root path's scope and is a module or package
    2. This prevents some quirky behavior where the LSP returns definitions from things like .venv
    """
    return os.path.commonpath([path, root_path]) == root_path


def get_all_paths_from_root_relative(root_path):
    abs_paths, rel_paths = [], []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            abs_path = os.path.join(root, file)
            relpath = os.path.relpath(abs_path, root_path)
            abs_paths.append(abs_path)
            rel_paths.append(relpath)
    return abs_paths, rel_paths


def create_lsp_client_instance(root_path, language) -> SyncLanguageServer:
    abs_root_path = os.path.abspath(root_path)
    config = MultilspyConfig.from_dict({"code_language": language})
    logger = MultilspyLogger()
    return SyncLanguageServer.create(config, logger, abs_root_path)


def get_language_from_ext(path):
    root, ext = os.path.splitext(path)
    language_info = EXT_TO_LANGUAGE_DATA.get(ext, {})
    is_code = language_info.get("is_code", False)
    language = language_info.get("language_mode", None)
    lsp_language = LANGUAGE_TO_LSP_LANGUAGE_MAP.get(language, None)
    return lsp_language, language, is_code


def keep_file_for_language(root, file, language):
    file_language, _, is_code = get_language_from_ext(file)
    if file_language == language and is_code:
        return True
    match language:
        case "javascript" | "typescript":
            if file.endswith("config.json") or file.endswith("package.json"):
                print("CallGraphBuilder :: keeping file: ", os.path.join(root, file))
                return True
        case _:
            return False


def copy_and_split_root_by_language_group(abs_root_path):
    abs_paths, _ = get_all_paths_from_root_relative(abs_root_path)
    languages = set()

    for p in abs_paths:
        lsp_language, language, is_code = get_language_from_ext(p)
        if is_code:
            languages.add(lsp_language)
    languages = [lang for lang in languages if lang]
    num_root_copies = len(languages)

    copy_paths = []
    # copy the root directory num_root_copies times into /tmp/callgraph_root_copies/{random_hash}
    for _ in range(num_root_copies):
        random_hash = str(uuid.uuid4()).split("-")[0]
        root_copy_path = os.path.join(TMP_DIR_PARENT, random_hash)
        shutil.copytree(abs_root_path, root_copy_path)
        copy_paths.append(root_copy_path)

    for copy_path, language in zip(copy_paths, languages):
        for root, dirs, files in os.walk(copy_path):
            for file in files:
                if keep_file_for_language(root, file, language):
                    continue
                else:
                    # print(f"removing file: {os.path.join(root, file)}")
                    os.remove(os.path.join(root, file))

    # remove copy_paths that only have directories and no files
    nonempty_copy_paths = []
    for copy_path, language in zip(copy_paths, languages):
        files_set = set()
        for root, dirs, files in os.walk(copy_path):
            for file in files:
                files_set.add(file)
        if not files_set:
            print(f"copy_path: {copy_path} is empty")
            shutil.rmtree(copy_path)
            continue
        nonempty_copy_paths.append((copy_path, language))

    return nonempty_copy_paths


def convert_to_relative_path(abs_path, root_path):
    # Ensure both paths are absolute
    abs_path = os.path.abspath(abs_path)
    root_path = os.path.abspath(root_path)
    try:
        rel_path = os.path.relpath(root_path, start=abs_path)
        return rel_path
    except ValueError as e:
        print(f"Error converting absolute path to relative path: {e}")
        return abs_path


def flatten(xss):
    return [x for xs in xss for x in xs]


## CALLGRAPH SPECIFIC UTILS


def get_containing_def_for_ref(defs: List[Definition], ref_range: Range):
    # find smallest range that contains ref
    containing_defs: List[Definition] = []
    for defn in defs:
        if defn.snippet_range.contains(ref_range):
            containing_defs.append(defn)
    if not containing_defs:
        return None
    return min(containing_defs, key=lambda x: x.snippet_range.height())


def get_node_id_for_viz(defn: Definition):
    node_id = f"{defn.path}::"
    node_id += f"{defn.range.start_line}-{defn.range.end_line}::"
    node_id += f"{defn.range.start_column}-{defn.range.end_column}"
    return node_id


def stable_hash(obj: dict, as_int=False, slice_size=16) -> str | int:
    """
    Creates a stable SHA-256 hash from a dictionary by:
    1. Converting to JSON with sorted keys
    2. Encoding to bytes
    3. Generating SHA-256 hash
    """
    # Convert dict to JSON string with sorted keys for consistency
    json_str = json.dumps(obj, sort_keys=True)
    # Create SHA-256 hash
    bytestr = hashlib.sha256(json_str.encode("utf-8")).hexdigest()
    if as_int:
        if slice_size is None:
            return int(bytestr, 16)
        if slice_size > 0:
            return int(bytestr[:slice_size], 16)
        raise ValueError(f"Invalid slice_size: {slice_size}")
    return bytestr
