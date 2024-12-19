import os
import yaml
from types import SimpleNamespace
from dataclasses import dataclass


class Utils:
        
    @staticmethod
    def dict_to_namespace(data: dict) -> SimpleNamespace:
        ns = SimpleNamespace()
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(ns, key, Utils.dict_to_namespace(value))
            else:
                setattr(ns, key, value)
        return ns
    
    @staticmethod
    def yaml_to_namespace(file_path: str) -> SimpleNamespace:
        assert os.path.exists(file_path), f"The file should exist, cannot read {file_path}"
        assert os.path.isfile(file_path), f"Should specify a valid file, got {file_path}"
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return Utils.dict_to_namespace(data)
        

    
    @classmethod
    def override_namespace(cls, ns_be_overriden: SimpleNamespace, ns_to_override: SimpleNamespace):
        for attr, value in ns_to_override.__dict__.items():
            if isinstance(value, SimpleNamespace):
                cls.override_namespace(getattr(ns_be_overriden, attr), value)
            else:
                setattr(ns_be_overriden, attr, value)


@dataclass
class ConfigNestManifest:
    selection_mode: str = "all"
    if_no_selection: str = "error"
    default_selection: str = None

    def select_all(self) -> bool:
        return self.selection_mode == "all"
    
    def select_one(self) -> bool:
        return not self.select_all()
    
    def skip_if_no_selection(self) -> bool:
        return self.if_no_selection == "skip"
    
    def error_if_no_selection(self) -> bool:
        return self.if_no_selection == "error"
    
    def get_default_selection(self) -> str:
        if self.if_no_selection == "default":
            return self.default_selection
        else:
            return None
    
    @classmethod
    def load_manifest(cls, manifest_filepath: str):
        if os.path.exists(manifest_filepath):
            return ConfigNestManifest(**Utils.yaml_to_namespace(manifest_filepath).__dict__)
        else:
            return ConfigNestManifest()


class ConfigNest:
    manifest_filename = "__confignest_manifest__"
    select_field = "__select__"
    override_field = "__override__"
    yaml_suffix = ".yaml"
    inherit_field = "__inherit__"

    def __init__(self, nest_root: str, view_file_path: str):
        self.nest_root = nest_root
        self.view = Utils.yaml_to_namespace(view_file_path)
        self.nest_instance = SimpleNamespace()
        self.parse(self.view, self.nest_instance, self.nest_root)
    
    def format_string(self):
        def _internal_format(ns: SimpleNamespace, prefix='\t'):
            s = ""
            for attr, value in ns.__dict__.items():
                if isinstance(value, SimpleNamespace):
                    s += f"{prefix}+ {attr}\n"
                    s += _internal_format(value, prefix + '|   ')
                else:
                    s += f"{prefix}- {attr}: {value}\n"
            return s
        return _internal_format(self.nest_instance)
    
    def export_flatten_namespace(self):
        def _internal_flatten(ns: SimpleNamespace, export_ns: SimpleNamespace):
            for attr, value in ns.__dict__.items():
                if isinstance(value, SimpleNamespace):
                    _internal_flatten(value, export_ns)
                else:
                    setattr(export_ns, attr, value)
            return export_ns
        
        return _internal_flatten(self.nest_instance, SimpleNamespace())

    
    @staticmethod
    def get_field(current_namespace: SimpleNamespace, field: str):
        if current_namespace is None:
            return None
        if hasattr(current_namespace, field):
            return current_namespace.__dict__.get(field)
        else:
            return None
    
    @classmethod
    def build_name_target_map(cls, current_folder: str):
        dl = os.listdir(current_folder)
        name_target_map = {}
        for target in dl:
            if target == cls.manifest_filename:
                continue
            if target.endswith(cls.yaml_suffix):
                name = target.replace(cls.yaml_suffix, "")
            else:
                name = target
            assert name not in name_target_map, f"Should not have same name of yaml file and folder in a same path, {dl}"
            name_target_map[name] = target
        return name_target_map
    
    @classmethod
    def load_manifest_from_file(cls, current_nest_path):
        manifest_filepath = os.path.join(current_nest_path, cls.manifest_filename)
        return ConfigNestManifest.load_manifest(manifest_filepath)

    
    @classmethod
    def parse(cls, current_view, current_nest_instance, current_nest_path):
        
        current_manifest = cls.load_manifest_from_file(current_nest_path)

        select_field_value = cls.get_field(current_view, cls.select_field)
        if select_field_value is not None:
            current_manifest.selection_mode = "one"
        override_field_value = cls.get_field(current_view, cls.override_field)

        current_name_target_map = cls.build_name_target_map(current_nest_path)

        if current_manifest.select_one():
            if select_field_value is None:
                if current_manifest.error_if_no_selection():
                    raise ValueError(f"Expect to select one in {current_name_target_map}, nest path: {current_nest_path}")
                elif current_manifest.skip_if_no_selection():
                    return
                else:
                    # use the default selection
                    select_field_value = current_manifest.get_default_selection()
            if select_field_value in current_name_target_map:
                current_name_target_map = {
                    select_field_value: current_name_target_map[select_field_value]
                }
            else:
                raise ValueError(f"{select_field_value} not in {current_name_target_map.keys()}")
        
        for name, target in current_name_target_map.items():
            target_path = os.path.join(current_nest_path, target)
            if os.path.isdir(target_path):
                setattr(current_nest_instance, name, SimpleNamespace())
                next_nest_instance = getattr(current_nest_instance, name)
                cls.parse(
                    cls.get_field(current_view, name),
                    next_nest_instance,
                    target_path
                )
            elif os.path.isfile(target_path):
                ns = Utils.yaml_to_namespace(target_path)
                # handle inherit
                if hasattr(ns, cls.inherit_field):
                    inherit_filename = getattr(ns, cls.inherit_field)
                    delattr(ns, cls.inherit_field)
                    inherit_ns = Utils.yaml_to_namespace(os.path.join(current_nest_path, inherit_filename))
                    if inherit_ns is not None:
                        Utils.override_namespace(inherit_ns, ns)
                        ns = inherit_ns
                    else:
                        raise ValueError(f"Inherit file {inherit_filename} not found in {current_nest_path}")
                if override_field_value is not None:
                    Utils.override_namespace(ns, override_field_value)
                inline_override = cls.get_field(current_view, name)
                if inline_override is not None:
                    Utils.override_namespace(ns, inline_override)
                
                if current_manifest.select_one():
                    Utils.override_namespace(current_nest_instance, ns)
                else:
                    setattr(current_nest_instance, name, ns)
            else:
                pass
