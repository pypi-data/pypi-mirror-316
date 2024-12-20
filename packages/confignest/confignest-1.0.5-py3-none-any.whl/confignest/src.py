import os
import yaml
from types import SimpleNamespace
from dataclasses import dataclass



class ConfigNestUtils:
        
    @staticmethod
    def dict_to_namespace(data: dict) -> SimpleNamespace:
        ns = ConfigNestNamespace()
        for key, value in data.items():
            if isinstance(value, dict):
                setattr(ns, key, ConfigNestUtils.dict_to_namespace(value))
            else:
                setattr(ns, key, value)
        return ns
    
    @staticmethod
    def yaml_to_namespace(file_path: str) -> SimpleNamespace:
        assert os.path.exists(file_path), f"The file should exist, cannot read {file_path}"
        assert os.path.isfile(file_path), f"Should specify a valid file, got {file_path}"
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        return ConfigNestUtils.dict_to_namespace(data)
        

    
    @classmethod
    def override_namespace(cls, ns_be_overriden: SimpleNamespace, ns_to_override: SimpleNamespace):
        for attr, value in ns_to_override.__dict__.items():
            if isinstance(value, ConfigNestNamespace):
                cls.override_namespace(getattr(ns_be_overriden, attr), value)
            else:
                setattr(ns_be_overriden, attr, value)
    
    @classmethod
    def format_namespace(cls, ns: SimpleNamespace, prefix='\t'):
        s = ""
        for attr, value in ns.__dict__.items():
            if isinstance(value, ConfigNestNamespace):
                s += f"{prefix}+ {attr}\n"
                s += cls.format_namespace(value, prefix + '|   ')
            else:
                s += f"{prefix}- {attr}: {value}\n"
        return s
    
    @classmethod
    def flatten_namespace(cls, ns: SimpleNamespace, export_ns: SimpleNamespace = None):
        if export_ns is None:
            export_ns = ConfigNestNamespace()
        for attr, value in ns.__dict__.items():
            if isinstance(value, ConfigNestNamespace):
                cls.flatten_namespace(value, export_ns)
            else:
                setattr(export_ns, attr, value)
        return export_ns


class ConfigNestNamespace(SimpleNamespace):
    def format_string(self):
        return ConfigNestUtils.format_namespace(self)
    
    def export_flatten(self):
        return ConfigNestUtils.flatten_namespace(self)



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
            return ConfigNestManifest(**ConfigNestUtils.yaml_to_namespace(manifest_filepath).__dict__)
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
        self.view = ConfigNestUtils.yaml_to_namespace(view_file_path)
        self.nest_instance = ConfigNestNamespace()
        self.parse(self.view, self.nest_instance, self.nest_root)
    
    def format_string(self):
        return self.nest_instance.format_string()
    
    def export_flatten_namespace(self):
        return self.nest_instance.export_flatten()

    
    @staticmethod
    def get_field(current_namespace: ConfigNestNamespace, field: str):
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
    def handle_inherit(cls, current_nest_path, target):
        target_path = os.path.join(current_nest_path, target)
        ns = ConfigNestUtils.yaml_to_namespace(target_path)
        if ns is None:
            raise ValueError(f"Inherit file {target} not found in {current_nest_path}")
        if not hasattr(ns, cls.inherit_field):
            return ns
        else:
            inherit_filename = getattr(ns, cls.inherit_field)
            delattr(ns, cls.inherit_field)
            inherit_ns = cls.handle_inherit(current_nest_path, inherit_filename)
            ConfigNestUtils.override_namespace(inherit_ns, ns)
            return inherit_ns
            

    
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
                setattr(current_nest_instance, name, ConfigNestNamespace())
                next_nest_instance = getattr(current_nest_instance, name)
                cls.parse(
                    cls.get_field(current_view, name),
                    next_nest_instance,
                    target_path
                )
            elif os.path.isfile(target_path):
                ns = cls.handle_inherit(current_nest_path, target)
                if override_field_value is not None:
                    ConfigNestUtils.override_namespace(ns, override_field_value)
                inline_override = cls.get_field(current_view, name)
                if inline_override is not None:
                    ConfigNestUtils.override_namespace(ns, inline_override)
                
                if current_manifest.select_one():
                    ConfigNestUtils.override_namespace(current_nest_instance, ns)
                else:
                    setattr(current_nest_instance, name, ns)
            else:
                pass
